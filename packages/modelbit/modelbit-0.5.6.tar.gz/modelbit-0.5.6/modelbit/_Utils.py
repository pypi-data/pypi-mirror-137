def _printMk(str):
  from IPython.display import display, Markdown
  display(Markdown(str))

def _printError(txt):
  _printMk(f'<span style="font-weight: bold; color: #E2548A;">Error:</span> {txt}')

# From https://stackoverflow.com/questions/1094841/get-human-readable-version-of-file-size
def _sizeof_fmt(num):
  if type(num) != int: return ""
  for unit in ["", "KB", "MB", "GB", "TB", "PB", "EB", "ZB"]:
    if abs(num) < 1000.0:
      return f"{num:3.0f} {unit}"
    num /= 1000.0
  return f"{num:.1f} YB"

def formatImageTag(imageUrl, imageAltText):
  imageUrl = imageUrl if imageUrl else "https://app.modelbit.com/images/profile-placeholder.png"
  return (
    f'<img src="{ imageUrl }" '
    f'alt="{ imageAltText }" '
    f'style="display:inline-block;border-radius:9999px;width:2rem;height:2rem;background-color: rgb(229 231 235);" />'
  )
