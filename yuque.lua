function Image(img)
    print("start download image", img.src)
    local imagePath = pandoc.pipe("python", {"image_replace.py", img.src}, "")
    img.src = imagePath
    print("image is download to", imagePath)
    return img
end

function RawInline(elem)
    return pandoc.SoftBreak()
end