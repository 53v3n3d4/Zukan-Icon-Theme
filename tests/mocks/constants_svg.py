SVG_ALL_UNUSED = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" xmlns:serif="http://www.serif.com/" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub1" serif:id="afpub"></g>
</svg>"""

SVG_ALMOST_CLEAN = """
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
xml:space="preserve" xmlns:serif="http://www.serif.com/"
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub1" serif:id="afpub"></g>
</svg>"""

SVG_CLEANED = """
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1" 
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" 
xml:space="preserve" 
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
<g id="afpub"></g>
</svg>"""

SVG_PARTIAL_UNUSED = """
<?xml version="1.0" encoding="UTF-8" standalone="no"?>
<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">
<svg width="100" height="100" viewBox="0 0 18 16" version="1.1"
xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink"
xml:space="preserve" xmlns:serif="http://www.serif.com/"
style="fill-rule:evenodd;clip-rule:evenodd;stroke-linejoin:round;stroke-miterlimit:2;">
<circle id="circle1" cx="50" cy="50" r="25" style="fill:red;">
</svg>"""

UNUSED_LIST = {
    '<?xml version="1.0" encoding="UTF-8" standalone="no"?>',
    '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
    ' xmlns:serif="http://www.serif.com/"',
}
