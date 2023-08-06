from . import _Utils
import pyaes

class _MbDatasets:
  _mbMain = None
  _datasets = []
  _iter_current = -1

  def __init__(self, mbMain):
    self._mbMain = mbMain
    resp = self._mbMain._getJsonOrPrintError("jupyter/v1/datasets/list")
    if resp:
      self._datasets = resp["datasets"]

  def _repr_markdown_(self):
    return self._makeDatasetsMkTable()

  def __iter__(self):
    return self

  def __next__(self):
    self._iter_current += 1
    if self._iter_current < len(self._datasets):
      return self._datasets[self._iter_current]["name"]
    raise StopIteration

  def _makeDatasetsMkTable(self):
    import timeago, datetime
    if len(self._datasets) == 0: return ""

    formatStr = "| Name | Owner | Data Refreshed | SQL Updated | Rows | Bytes | \n" + \
      "|:-|:-:|-:|-:|-:|-:|\n"
    for d in self._datasets:
      dataTimeVal = ''
      sqlTimeVal = ''
      numRows = d["numRows"] if "numRows" in d else None
      numBytes = d["numBytes"] if "numBytes" in d else None
      ownerInfo = d["ownerInfo"]
      ownerImageTag = _Utils.formatImageTag(
        ownerInfo["imageUrl"], ownerInfo["name"]
      )

      if 'recentResultMs' in d and d["recentResultMs"] != None:
        dataTimeVal = timeago.format(datetime.datetime.fromtimestamp(d["recentResultMs"]/1000), datetime.datetime.now())
      if 'sqlModifiedAtMs' in d and d["sqlModifiedAtMs"] != None:
        sqlTimeVal = timeago.format(datetime.datetime.fromtimestamp(d["sqlModifiedAtMs"]/1000), datetime.datetime.now())
      formatStr += f'| { d["name"] } | { ownerImageTag } | { dataTimeVal } | { sqlTimeVal } |' + \
        f' { self._fmt_num(numRows) } | {_Utils._sizeof_fmt(numBytes)} |\n'
    return formatStr

  def get(self, dsName):
    from urllib.parse import quote_plus
    import io, pandas
    data = self._mbMain._getJsonOrPrintError(f'jupyter/v1/datasets/get?dsName={quote_plus(dsName)}')
    if not data: return

    try:
      self._storeDatasetResultIfMissing(dsName,
        data["dsrDownloadInfo"]["id"], data["dsrDownloadInfo"]["signedDataUrl"])
      rawDecryptedData = self._decryptUnzipFile(data["dsrDownloadInfo"]["id"], 
        data["dsrDownloadInfo"]["key64"], data["dsrDownloadInfo"]["iv64"])
    except Exception as err:
      _Utils._printMk(f'_Error fetching dataset. Please try again. ({err})_')
      self._clearTmpFile(data["dsrDownloadInfo"]["id"])
      return None

    stStream = io.BytesIO(rawDecryptedData)
    df = pandas.read_csv(stStream, sep='|', low_memory=False, na_values=['\\N', '\\\\N'])
    return df

  def _dsFilepath(self, dsId):
    import tempfile, os
    mbTempDir = os.path.join(tempfile.gettempdir(), 'modelbit')
    if not os.path.exists(mbTempDir):
      os.makedirs(mbTempDir)
    return os.path.join(mbTempDir, dsId)

  def _storeDatasetResultIfMissing(self, dsName, dsId, url):
    import urllib.request, os, sys, ssl
    from tqdm import tqdm

    filepath = self._dsFilepath(dsId)
    if os.path.exists(filepath):
      return

    _Utils._printMk(f'_Downloading "{dsName}"..._')
    class DownloadProgressBar(tqdm): # From https://github.com/tqdm/tqdm#hooks-and-callbacks
      def update_to(self, b=1, bsize=1, tsize=None):
          if tsize is not None:
              self.total = tsize
          self.update(b * bsize - self.n)
    with DownloadProgressBar(unit='B', unit_scale=True, miniters=1, desc="", file=sys.stdout) as t:
      default_context = ssl._create_default_https_context
      try:
        urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)
      except:
        # In case client has local SSL cert issues: pull down encrypted file without cert checking
        self._clearTmpFile(dsId)
        ssl._create_default_https_context = ssl._create_unverified_context
        urllib.request.urlretrieve(url, filename=filepath, reporthook=t.update_to)
      finally:
        ssl._create_default_https_context = default_context

  def _clearTmpFile(self, dsId):
    import os
    filepath = self._dsFilepath(dsId)
    if os.path.exists(filepath):
      os.remove(filepath)

  def _decryptUnzipFile(self, dsId, key64, iv64):
    from Cryptodome.Cipher import AES
    import os, base64, zlib, io
    filepath = self._dsFilepath(dsId)
    if not os.path.exists(filepath):
      _Utils._printMk(f'**Error:** Couldn\'t find local data at {filepath}')

    try:
      cipher = AES.new(base64.b64decode(key64), AES.MODE_CBC, iv=base64.b64decode(iv64))
      fileIn = open(filepath, 'rb')
      raw = fileIn.read()
      fileIn.close()
      return zlib.decompress(cipher.decrypt(raw), zlib.MAX_WBITS|32)
    except Exception as err:
      # Fallback needed to support: Windows 11 on Mac M1 in Parallels
      _Utils._printMk(f"Warning: Falling back to pure-Python decryption.")
      mode = pyaes.AESModeOfOperationCBC(base64.b64decode(key64), iv=base64.b64decode(iv64))
      outStream = io.BytesIO()
      pyaes.decrypt_stream(mode, io.BytesIO(raw), outStream)
      outStream.seek(0)
      return zlib.decompress(outStream.read(), zlib.MAX_WBITS|32)

  def _fmt_num(self, num):
    if type(num) != int: return ""
    return format(num, ",")

