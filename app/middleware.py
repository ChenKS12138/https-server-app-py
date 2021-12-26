from typing import Callable

from infra.http.message import Request, Response
from infra.http.form_data import FormData
from infra.http.method import get_method, Method
import infra.http.status as status
from jinja2 import Template
from os import path, listdir, remove
from shutil import rmtree


ICON_FILE = u"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAABgAAAAYCAYAAADgdz34AAAABmJLR0QA/wD/AP+gvaeTAAAAcklEQVRIie3VQQqAIBCF4b/ocB6rZefUg9hGoURtZiIC8YG4cGY+VwojxgEBiA9rtwJeMPwVkpslNRE4vgbUiAVQIVagiiyN5tZZWVPLrW/rXVM6pIeuRkCcCUxgAj8BIe3ST+f6OAYEceh+tbx86h0sJ1orUB8gNFrWAAAAAElFTkSuQmCC"
ICON_DIR = u"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAABCUlEQVRoge2ZTQ4BMRiGHyIkTuAUVjY4g4VD+VtZuZiVAzAcQWxY6MRkNLQM/cj7JF86aTrJ+3S+ZhYFIUQoTWABZMA5oDJgnCTpE+aECRTrBPRShH3Ejmu4fuD6pVu/AdqfCvUK+S6H0gLW7p3VRxK9SKwIQBc4Et+S79YOmHE915WIAIy4teW3a1qlSAoG3L7MHb8kAqW89YRBKqXhmdsDnW8HieRQnqgVnn+prYrUyhN5z4X+EFOSH3bv5uuwW0Ai1pCINSRiDYlYQyLWkIg1JGINiVhDItaQiDUkYg2JWOMvRTI3DlIEiWToRu9Fz4w012fv1MQn0nQyqe4DY2rrJLyXoUKIey7M1NDZgDzGvQAAAABJRU5ErkJggg=="
ICON_SYMLINK = u"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAACDElEQVRoge2Yu0rEQBSGv/UComLngloJa2ch1t5gn0DQUixsvFQ+gXaCla1PIAj6ACouaqFiIbp46XwCLRQsVlGLnGC87SZzy7jkQJjM7Jl//i+TmSQLWfyveLd43ABd9QDiFCYc0JauMxjbIOVImbcwzo8Bbel2Apc4mBnbIOAIxgUIOIBxBQKWYVyCgEUY1yBgCSYNELAAkxYIGIZx8WSPe5SrCeZiDBgnL2moXpw/fTQpCupG0gtTE7xB0Yh3kYH4FrZA9om/Gx1Z8vAlVLffU5JtrbZ8aAvEfZh5DwLBF9+V9D/T1K+ZZ3OxDwDdcv5qcZxYoTojC8CL9N0A2jX1U7m1poE3gllYNKTvHGQUqEif+V9+7ydYL8cEa8hLkGbgVvJXfvl9BniOaJbxFGRScq8JoMLIAasRrW2+QngHsim5c9/a16T9DVgmAMvj8YzcSW5fpG1W2irAxLf8PHAC7Br2oS0Q3v8tUu8BHqVtSsdEQh/aAqHpDqkvSX1Lx4CCD22BcMcalPq51Md0DMT1YfIV5VDKcSl7pTw3OIZyJJmRouQ+ECzkJ6m3OvZhRKAk+TvAhZwP6xhQ9KEtUADupc+rlLtAo44JBR9GBIb4hAmPPWAEaHPow4hAgb+/20sOfRgTKALrBO9f4eI/SMGHvoChSPVT12lkIL5F3H/jfVgnVaNuZiQL3+ID+YBWVoOW43UAAAAASUVORK5CYII="
ICON_UNKNOWN = u"data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAADIAAAAyCAYAAAAeP4ixAAAABmJLR0QA/wD/AP+gvaeTAAACXUlEQVRoge3ZPWsUQRzH8c/FCBKIlYVYKKiIGnxAlCiC+FRoEcVKjC9AEMGARHwLYuML0BdhYyoLHwIS0SKYJmiTNPGBKEiiQfEslkQNO7s7d7e3F7gvTDPH/v6/397s7MxsTWvpwSDO4RS2YDN68QWTeINHeNni2i1hHYYxhXrB9hZXUavAbyrbMaF4gNXtKXa03fUqLuKrxkMst0843mbvK1zCzxyDMe07jrU1AfZhoUnjaW0O29oVoobxHEOTuI7d6EM/jmAU0znXjrUryJUME4u4Jnsm6sVt2cNyqCTvK/TgfaD4Es5GaF0QDvOsdZbTOR0oXMfNBvTuBLR+Y2cL/Aa5Fyg8JRkysazHu4DmSIxQT2Tho4H+h/gVqUUytB4EfjvYgF5h5qTfvYEmNAcDmq+acprDUqBofxOamwKa0zEisUPrY0rfLL5F6vxLPdC/oQnNXM5jxt+7NiNZsjfDYen/yOsYkdiZZgxbI6/J40ygf7bFdUqlV3j6Ha3QVzShF2Id+yv0FcWQ8BJlokJfhenBLdmLxsuVuSvIIcmhQ9Yy/okO2senMSJ/R/lZB+zfs7grO0AdP3CiKoNFuCE/xDxOVmWwCAOSQ4WsEM+xqyqDRXksHGBBsq/v6AcbDgiHmMWe6qzFEXrAFyXT8JohdIx6v0pTsdQk02lakL0V+opmo/QQSxo7pMgldodYlL5A/7zGDilyKStI2+kG6TS6QTqNsoLMS97gq1lTJyPLDOOD/08OQ2fHXbp0WcOkffl9UVaxMreZoc8FpdTsvhA7jW6QAoyn9JX2sP8BoWVXVMudA50AAAAASUVORK5CYII="


def get_icon(p: str) -> str:
    if path.isfile(p):
        return ICON_FILE
    elif path.isdir(p):
        return ICON_DIR
    elif path.islink(p):
        return ICON_SYMLINK
    else:
        return ICON_UNKNOWN


def static_middleware(root: str) -> Callable[[Request], Response]:
    not_found = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
    <body>
        <h1>Not Found {{ path }}</h1>  
    </body>
</html>""")

    unknown = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
    <body>
        <h1>Unknown Forbidden {{ path }}</h1> 
    </body>
</html>""")

    index = Template("""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta http-equiv="X-UA-Compatible" content="IE=edge">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{{ title }}</title>
</head>
    <body>
        <script>
        function deleteFile(filepath) {
            if(!confirm('Sure To Delete '+filepath)) return;
            var xhr = new XMLHttpRequest();
            if(onload) {
                xhr.onload = onload;
            }
            xhr.open("delete",filepath,true);
            xhr.send(null);
            xhr.onload = function(){
                location.reload();
            }
        }
        function uploadFile(filepath,file,onload){
            if(!confirm('Sure To Upload '+filepath)) return;
            var xhr = new XMLHttpRequest();
            if(onload) {
                xhr.onload = onload
            }
            xhr.open("post",filepath,true);
            xhr.setRequestHeader("Content-Type","multipart/form-data; boundary=----WebKitFormBoundaryyb1zYhTI38xpQxBK");
            var formData = new FormData();
            formData.append("file", file);
            xhr.send(formData);
        }
        </script>
        <h1>Index {{ path }}</h1>
        <ul>
            <li>
                <a href="../">../</a>
            </li>
            {% for file in files  %}
                <li>
                    <button onclick="deleteFile('{{file[1]}}')" >delete</button>
                    <img width="20" src="{{file[2]}}" />
                    <a href="{{file[1]}}" >{{file[0]}}</a>
                </li>
            {% endfor %}
        </ul>
        <input id="file" type="file" />
        <button id="upload" disabled >上传</button>
        <script>
        var fileInput = document.getElementById("file");
        var uploadBtn = document.getElementById("upload")
        fileInput.addEventListener("change",function(){
            uploadBtn.disabled=false;
        });
        uploadBtn.addEventListener("click",function(){
            var file = fileInput.files.length && fileInput.files[0];
            if(!file) return;
            var prefix = "{{ path }}".replace(/\\/$/,"");
            uploadFile(prefix+"/"+file.name,file, function() {
                fileInput.value = '';
                location.reload();
            });
        });
        </script>
    </body>
</html>""")

    def get_handler(request: Request) -> Response:
        current = path.join(path.abspath(
            root), request.path[1:].replace("../", ""))
        response = Response(
            headers={"Content-Type": "text/html"}, code=status.OK, body=bytes())

        if not path.exists(current):
            response.body = not_found.render(
                title="Not Found"+request.path, path=request.path).encode()
        else:
            files = [(item, path.join(request.path, item), get_icon(path.join(current, item)))
                     for item in listdir(current)]
            response.body = index.render(
                title=request.path, path=request.path, files=files).encode()

        return response

    def post_handler(request: Request) -> Response:
        current = path.join(path.abspath(
            root), request.path[1:].replace("../", ""))
        data: FormData = FormData.parse(request.body)
        bad_request = Response(headers={
                               "Content-Type": "text/html"}, code=status.BAD_REQUEST, body="Bad Request".encode())
        ok = Response(headers={"Content-Type": "text/plain"},
                      code=status.OK, body="ok".encode())
        if data == None:
            return bad_request
        upload_file = data.get_part("file")
        if upload_file == None:
            return bad_request
        with open(current, 'w+b') as f:
            f.write(upload_file.data)
        return ok

    def delete_handler(request: Request) -> Response:
        current = path.join(path.abspath(
            root), request.path[1:].replace("../", ""))
        bad_request = Response(headers={
                               "Content-Type": "text/html"}, code=status.BAD_REQUEST, body="Bad Request".encode())
        ok = Response(headers={"Content-Type": "text/plain"},
                      code=status.OK, body="ok".encode())
        if not path.exists(current):
            return bad_request
        elif path.isdir(current):
            rmtree(current)
            return ok
        else:
            remove(current)
            return ok

    def handler(request: Request) -> Response:
        if request.method == get_method(Method.Get):
            return get_handler(request)
        elif request.method == get_method(Method.Post):
            return post_handler(request)
        elif request.method == get_method(Method.Delete):
            return delete_handler(request)
        else:
            return Response(headers={"Content-Type": "text/html"}, code=status.METHOD_NOT_ALLOWED, body="Method Not Allowed".encode())

    return handler
