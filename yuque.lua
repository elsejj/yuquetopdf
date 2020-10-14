function Image(img)
    local imagePath = pandoc.pipe("python", {"image_replace.py", img.src}, "")
    img.src = imagePath
    return img
end

function RawInline(elem)
    return pandoc.SoftBreak()
end