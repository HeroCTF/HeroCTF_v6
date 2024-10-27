local function url_decode(s)
    s = s:gsub("%%(%x%x)", function(hex)
        local char_code = tonumber(hex, 16)
        if char_code >= 0x21 and char_code <= 0x7F then
            return string.char(char_code)
        else
            return "%" .. hex
        end
    end)
    return s
end

core.register_action("security", { "http-req" }, function(txn)
    local path = txn.sf:path()
    path = url_decode(path)

    if path:find("..", 1, true) then
        txn.http:req_set_path("/403.html")
        return
    end

    txn.http:req_set_path(path)
end)
