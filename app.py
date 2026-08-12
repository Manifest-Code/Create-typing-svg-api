from click import pause
from flask import Flask, request, Response # Request -let your Python program send HTTP requests to other servers/APIs.
                                           # Response - lets you send HTTP responses back to the client.
from xml.sax.saxutils import escape
import re      # is a Python statement that imports the re module, which stands for regular expressions.
               #Regular expressions (regex) are patterns used to search, match, extract, or replace text.

app = Flask(__name__)

@app.route('/typing')       # creating route for the typing endpoint
def typing():

    ## =========================================
    # GET PARAMETERS
    # =========================================

    font = request.args.get("font", "Arial")
    size = request.args.get("size", "30")
    duration = request.args.get("duration", "3000")
    pause = request.args.get("pause", "1000")
    color = request.args.get("color", "EAB8E4")

    center = request.args.get("center", "false").lower() == "true"
    v_center = request.args.get("vCenter", "false").lower() == "true"

    width = request.args.get("width", "600")

    lines = request.args.get(
        "lines",
        "Hello World"
    ).split(";")


    # =========================================
    # VALIDATION
    # =========================================

    if not re.fullmatch(r"[0-9A-Fa-f]{6}", color):
        return "Invalid color. Use 6-digit hex color.", 400

    try:
        size = int(size)

        if size < 10 or size > 100:
            return "Size must be between 10 and 100.", 400

    except ValueError:
        return "Size must be a number.", 400


    try:
        width = int(width)

        if width < 100 or width > 1200:
            return "Width must be between 100 and 1200.", 400

    except ValueError:
        return "Width must be a number.", 400


    try:
        duration = int(duration)

        if duration <= 0:
            return "Duration must be greater than 0.", 400

    except ValueError:
        return "Duration must be a number.", 400


    try:
        pause = int(pause)

        if pause < 0:
            return "Pause cannot be negative.", 400

    except ValueError:
        return "Pause must be a number.", 400


    # =========================================
    # FONT
    # =========================================

    allowed_fonts = [
        "Arial",
        "Verdana",
        "Georgia",
        "Courier New",
        "Times New Roman",
        "Quicksand"
    ]

    if font not in allowed_fonts:
        font = "Arial"


    # =========================================
    # POSITION
    # =========================================

    if center:
        x_position = width / 2
        text_anchor = "middle"
    else:
        x_position = 20
        text_anchor = "start"

    if v_center:
        y_position = 55
    else:
        y_position = 60


    # =========================================
    # PREPARE TEXT FOR JAVASCRIPT
    # =========================================

    # Escape each line for safe insertion into JS
    safe_lines = []

    for line in lines:
        safe_lines.append(line)


    # Create JavaScript array safely
    import json

    lines_json = json.dumps(
        safe_lines,
        ensure_ascii=False
    )


    # =========================================
    # CREATE SVG
    # =========================================

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>

<svg
    xmlns="http://www.w3.org/2000/svg"
    width="{width}"
    height="100"
    viewBox="0 0 {width} 100">

    <style>

        #typingText {{
            font-family: "{font}", Arial, sans-serif;
            font-size: {size}px;
            fill: #{color};
        }}

    </style>


    <text
        id="typingText"
        x="{x_position}"
        y="{y_position}"
        text-anchor="{text_anchor}">
    </text>


    <script type="text/ecmascript"><![CDATA[

        const lines = {lines_json};

        const typingDuration = {duration};

        const pauseDuration = {pause};

        const textElement = document.getElementById("typingText");


        let lineIndex = 0;


        function typeLine() {{

            const line = lines[lineIndex];

            let characterIndex = 0;


            // Clear previous line
            textElement.textContent = "";


            // Calculate delay for each character
            const characterDelay =
                line.length > 0
                ? typingDuration / line.length
                : typingDuration;


            function typeCharacter() {{

                if (characterIndex < line.length) {{

                    textElement.textContent +=
                        line[characterIndex];

                    characterIndex++;

                    setTimeout(
                        typeCharacter,
                        characterDelay
                    );

                }} else {{

                    // Finished typing
                    setTimeout(
                        nextLine,
                        pauseDuration
                    );

                }}

            }}


            typeCharacter();

        }}


        function nextLine() {{

            lineIndex++;

            if (lineIndex >= lines.length) {{
                lineIndex = 0;
            }}

            typeLine();

        }}


        // Start animation
        typeLine();

    ]]></script>

</svg>
'''

    
    # SVG stands for Scalable Vector Graphics.
    return Response(svg, content_type="image/svg+xml") 
    # It's basically identifying what type of markup <svg> represents. It's a namespace identifier.
    #Response - Send the SVG content stored in svg back to the browser as an SVG image.
    #"Only start the Flask server when I directly run this Python file."

if __name__ == "__main__":    # Python automatically creates a special variable called __name__.
    app.run(debug=True)

# (uv run app.py )in terminal run this you will get Running on http://127.0.0.1:5000
# copy and try below various links
# http://127.0.0.1:5000/typing
# http://127.0.0.1:5000/typing?text=Hello world ✨
# http://127.0.0.1:5000/typing?text=Hello&size=40&color=00FF00&speed=5