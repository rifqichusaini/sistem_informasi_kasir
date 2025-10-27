from colorama import init, Fore, Back, Style

class StyleText:
  def __init__(self):
    init()

  def warning(self, string):
    return f'{Fore.RED}{string}{Style.RESET_ALL}'

  def approve(self, string):
    return f'{Fore.GREEN}{string}{Style.RESET_ALL}'

  def attention(self, string):
    return f'{Fore.BLACK}{Back.WHITE}{string}{Style.RESET_ALL}'