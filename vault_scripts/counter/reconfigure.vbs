' bbclone postinstall script
' required parameters: bbc_mainsite, bbc_show_config, bbc_titlebar,
'	bbc_language, bbc_maxtime, bbc_maxvisible,
'	bbc_maxos, bbc_maxbrowser, max_extension, bbc_maxrobot, bbc_maxpage,
'	bbc_maxorigin, bbc_ignoreip, bbc_ignore_refer, bbc_own_refer,
'	bbc_stat_field_id, bbc_stat_field_time, bbc_stat_field_visits,
'	bbc_stat_field_ext, bbc_stat_field_dns, bbc_stat_field_refer,
'	bbc_stat_field_os, bbc_stat_field_browser, bbc_general_align_style,
'	bbc_title_size, bbc_subtitle_size, bbc_text_size

' here is also some standard parameters, that must be specified:
' vhost_path - full path to vhost root directory
' domain_name - name of domain
' install_prefix - path of application inside vhost directory
' ssl_target_directory - true, if application is in httpsdocs

'on error resume next

' file system object
Dim FSO
' input parameters
Dim Params

Set FSO = CreateObject("Scripting.FileSystemObject")
Set Params = CreateObject("Scripting.Dictionary")
Set SysEnv = Shell.Environment("SYSTEM")

ReadParams
'PrintParams "C:\ScriptsOutput\output.txt"
CheckParams
ParseParams
BackupConfigFile
GenerateBbcloneConfig

Set Params = Nothing
Set FSO=Nothing
Set SysEnv = Nothing

WScript.Quit(err.number)

'------------------------------------
' read parameters from standard input
'------------------------------------
Sub ReadParams
	Params.RemoveAll
	Do While Not WScript.StdIn.AtEndOfStream
		Param = Trim(WScript.StdIn.ReadLine)
		Pos = InStr(Param, "=")
		Name = Mid(Param, 1, Pos - 1)
		Value = Mid(Param, Pos + 1)
		Params.Add Name, Value
	Loop
End Sub

Sub PrintParams(OutputFileName)
	Dim Output
	Set Output = FSO.CreateTextFile(OutputFileName, True)
	Dim Keys, Items
	Keys = Params.Keys()
	Items = Params.Items()
	For I = 0 To Params.Count - 1
		Output.WriteLine Keys(I) & "=" & Items(I)
	Next
	Output.Close
End Sub

' check existance of necessary parameters & add extra parameters
Sub CheckParams

	Dim Name, Names
	' necessary parameters
	Names = Array(_
		"vhost_path","domain_name","install_prefix","ssl_target_directory",_
		"bbc_mainsite")
	For Each Name In Names
		If Not Params.Exists(Name) Or Len(Params.Item(Name)) = 0 Then
			WScript.Echo "No " & Name & " parameter specified for application"
			
			WScript.Quit(1)
		End If
	Next
	
	' extra parameters
	Names = Array(_
		"documents_directory","document_root","bbcounter_config","proto",_
		"bbc_show_config", "bbc_titlebar","bbc_ignore_refer",_
		"bbc_language", "bbc_maxtime", "bbc_maxvisible",_
		"bbc_maxos","bbc_maxbrowser", "max_extension", "bbc_maxrobot", "bbc_maxpage",_
		"bbc_maxorigin",   "bbc_own_refer",_
		"bbc_stat_field_id", "bbc_stat_field_time", "bbc_stat_field_visits",_
		"bbc_stat_field_ext", "bbc_stat_field_dns", "bbc_stat_field_refer",_
		"bbc_stat_field_os", "bbc_stat_field_browser","bbc_general_align_style",_
		"bbc_title_size", "bbc_subtitle_size", "bbc_text_size","bbc_ignoreip")
	For Each Name In Names
		If Not Params.Exists(Name) Then
			Params.Add Name, ""
		End If
	Next
End Sub

Sub ParseParams
	

	If Params.Item("ssl_target_directory") = "true" Then
		Params.Item("documents_directory") = "httpsdocs"
		Params.Item("proto") = "https"
	Else
		Params.Item("documents_directory") = "httpdocs"
		Params.Item("proto") = "http"
	End If
	Params.Item("document_root") = Params.Item("vhost_path") & "\" & Params.Item("documents_directory")
	Params.Item("bbcounter_config") = Params.Item("document_root") & "\" & Params.Item("install_prefix")&"\conf\config.php"
End Sub

Sub BackupConfigFile
	
	If FSO.FileExists(PathName) And  Not FSO.FileExists(Params.Item("bbcounter_config")&".orig") Then
		FSO.MoveFile Params.Item("bbcounter_config"), Params.Item("bbcounter_config") & ".orig"
	End If
End Sub

Sub GenerateBbcloneConfig

'	WScript.StdOut.WriteLine Params.Item("bbcounter_config")
	Dim Config
	Set Config = FSO.CreateTextFile(Params.Item("bbcounter_config"), True)
	Config.WriteLine "<?php"
	Config.WriteLine "$BBC_MAINSITE = """&Params.Item("proto")&"://"&Params.Item("bbc_mainsite")&""";"
	if  Params.Item("bbc_show_config")<>"" Then
		Config.WriteLine "$BBC_SHOW_CONFIG = "&Params.Item("bbc_show_config")&";" 
	else
		Config.WriteLine "$BBC_SHOW_CONFIG = 1;" 
	end if
	
	if  Params.Item("bbc_titlebar")<>"" Then
		Config.WriteLine "$BBC_TITLEBAR = """&Params.Item("bbc_titlebar")&""";" 
	else
		Config.WriteLine "$BBC_TITLEBAR = ""Statistics for %SERVER generated the %DATE\"";"
	end if
	
	if Params.Item("bbc_language")<> ""  Then
		Config.WriteLine "$BBC_LANGUAGE =  """&Params.Item("bbc_language")&""";"
	else
		Config.WriteLine "$BBC_LANGUAGE = ""en"";"
	end if
	
	if Params.Item("bbc_maxtime")<> ""  Then
		Config.WriteLine "$BBC_MAXTIME = "&Params.Item("bbc_maxtime")&";"
	else
		Config.WriteLine "$BBC_MAXTIME = 1800;"
	end if
	
	if Params.Item("bbc_maxvisible")<> ""  Then
		Config.WriteLine "$BBC_MAXVISIBLE = "&Params.Item("bbc_maxvisible")&";"
	else
		Config.WriteLine "$BBC_MAXVISIBLE = 100;"
	end if
	
	if Params.Item("bbc_maxos")<> ""  Then
		Config.WriteLine "$BBC_MAXOS = "&Params.Item("bbc_maxos")&";"
	else
		Config.WriteLine "$BBC_MAXOS = 10;"
	end if
	
	if Params.Item("bbc_maxbrowser")<> ""  Then
		Config.WriteLine "$BBC_MAXBROWSER = "&Params.Item("bbc_maxbrowser")&";"
	else
		Config.WriteLine "$BBC_MAXBROWSER = 10;"
	end if
	
	if Params.Item("max_extension")<> ""  Then
		Config.WriteLine "$BBC_MAXEXTENSION = "&Params.Item("max_extension")&";"
	else
		Config.WriteLine "$BBC_MAXEXTENSION = 10;"
	end if
	
	if Params.Item("bbc_maxrobot")<> ""  Then
		Config.WriteLine "$BBC_MAXROBOT = "&Params.Item("bbc_maxrobot")&";"
	else
		Config.WriteLine "$BBC_MAXROBOT = 10;"
	end if
	
	if Params.Item("bbc_maxpage")<> ""  Then
		Config.WriteLine "$BBC_MAXPAGE = "&Params.Item("bbc_maxpage")&";"
	else
		Config.WriteLine "$BBC_MAXPAGE = 10;"
	end if
	
	if Params.Item("bbc_maxorigin")<> ""  Then
		Config.WriteLine "$BBC_MAXORIGIN = "&Params.Item("bbc_maxorigin")&";"
	else
		Config.WriteLine "$BBC_MAXORIGIN = 10;"
	end if
	
	Config.WriteLine "$BBC_IGNORE_IP = """&Params.Item("bbc_ignoreip")&""";"
	Config.WriteLine "$BBC_IGNORE_REFER = """&Params.Item("bbc_ignore_refer")&""";"
	
	if Params.Item("bbc_own_refer")<> ""  Then
		Config.WriteLine "$BBC_OWN_REFER = "&Params.Item("bbc_own_refer")&";"
	else
		Config.WriteLine "$BBC_OWN_REFER = 1;"
	end if
	
	Dim bbc_detailed_stat_fields
	
	bbc_detailed_stat_fields=""
	
	if Params.Item("bbc_stat_field_id")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", id"
	end if
	
	if Params.Item("bbc_stat_field_time")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", time"
	end if
	
	if Params.Item("bbc_stat_field_visits")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", visits"
	end if
	
	if Params.Item("bbc_stat_field_ext")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", ext"
	end if
	
	if Params.Item("bbc_stat_field_dns")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", dns"
	end if
	
	if Params.Item("bbc_stat_field_refer")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", referer"
	end if
	
	if Params.Item("bbc_stat_field_os")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", os"
	end if
	
	if Params.Item("bbc_stat_field_browser")<> ""  Then
		bbc_detailed_stat_fields = bbc_detailed_stat_fields&", browser"
	end if
	
	if bbc_detailed_stat_fields<>"" Then
		bbc_detailed_stat_fields=Mid(bbc_detailed_stat_fields,3)
	end if
	
	Config.WriteLine "$BBC_DETAILED_STAT_FIELDS = """&bbc_detailed_stat_fields&""";"
	
	if Params.Item("bbc_general_align_style")<> ""  Then
		Config.WriteLine "$BBC_GENERAL_ALIGN_STYLE = """&Params.Item("bbc_general_align_style")&""";"
	else
		Config.WriteLine "$BBC_GENERAL_ALIGN_STYLE = ""center"";"
	end if
	
	if Params.Item("bbc_title_size")<> ""  Then
		Config.WriteLine "$BBC_TITLE_SIZE = "&Params.Item("bbc_title_size")&";"
	else
		Config.WriteLine "$BBC_TITLE_SIZE = 4;"
	end if
	
	if Params.Item("bbc_subtitle_size")<> ""  Then
		Config.WriteLine "$BBC_SUBTITLE_SIZE = """&Params.Item("bbc_subtitle_size")&""";"
	else
		Config.WriteLine "$BBC_SUBTITLE_SIZE = ""2"";"
	end if
	
	if Params.Item("bbc_text_size")<> ""  Then' In UNIX version checking bbc_subtitle_size ???
		Config.WriteLine "$BBC_TEXT_SIZE = """&Params.Item("bbc_text_size")&""";"
	else
		Config.WriteLine "$BBC_TEXT_SIZE = ""1"";"
	end if
	
	Config.WriteLine "?>"
	Config.Close

End Sub
