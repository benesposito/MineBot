import win32com.client
oAutoItX = win32com.client.Dispatch( "AutoItX3.Control")

# oAutoItX.Opt("WinTitleMatchMode", 2) #Match text anywhere in a window title

list = oAutoItX.WinList()
print(list)
#
# width = oAutoItX.WinGetClientSizeWidth("Minecraft")
# height = oAutoItX.WinGetClientSizeHeight("Minecraft")
#
# print('{}, {}'.format(width, height))