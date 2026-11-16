Set WshShell = CreateObject("WScript.Shell")
strDesktop = WshShell.SpecialFolders("Desktop")
Set oLink = WshShell.CreateShortcut(strDesktop & "\MP4 to Images Studio.lnk")
Set FSO = CreateObject("Scripting.FileSystemObject")
strExe = WshShell.CurrentDirectory & "\MP4_to_Images_Studio.exe"

If FSO.FileExists(strExe) Then
    oLink.TargetPath = strExe
    oLink.Arguments = ""
Else
    oLink.TargetPath = "wscript.exe"
    oLink.Arguments = """" & WshShell.CurrentDirectory & "\Lancer_Application.vbs"""
End If

oLink.WorkingDirectory = WshShell.CurrentDirectory
oLink.IconLocation = WshShell.CurrentDirectory & "\icon.ico, 0"
oLink.Description = "MP4 to Images Studio - Decoupe et Extraction de sequences video"
oLink.Save
WScript.Echo "Raccourci avec icone cree avec succes sur votre Bureau !"
