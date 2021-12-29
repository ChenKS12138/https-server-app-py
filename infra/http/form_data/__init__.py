from typing import Optional, List
from infra.http.form_data.fsm import FormDataFSM, Input, Output, State

# 定义文件的文件格式类


class FormDataPart:
    name: Optional[str] = None
    filename: Optional[str] = None
    content_type: Optional[str] = None
    data: bytes = bytes()

    def __str__(self) -> str:
        return "name: {}, filename: {}, content_type: {}, data: {}".format(self.name, self.filename, self.content_type, self.data)

# 定义Formdata类(一般有多个文件)


class FormData:
    parts: List[FormDataPart] = list()
    boundary: bytes = bytes()

    def __str__(self) -> str:
        return "parts: {}, boundary: {}".format([str(part) for part in self.parts], self.boundary)

    def get_part(self, name: str) -> Optional[FormDataPart]:
        for item in self.parts:
            if item.name == name:
                return item
        return None

    # 定义解析formdata(即request.body)的函数，
    @staticmethod
    def parse(raw: bytes):
        machine = FormDataFSM()
        form_data = FormData()
        form_data_part = FormDataPart()
        header_field = bytes()
        header_value = bytes()
        boundary_like = bytes()

        for byte in raw:
            input = None
            if byte == ord('-') and machine.state != State.Boundary and machine.state != State.End and boundary_like == form_data.boundary:
                input = Input.EndDash
            elif (machine.state == State.Data or machine.state == State.DataToBoundary) and len(form_data.boundary) > len(boundary_like) and form_data.boundary[len(boundary_like)] == byte:
                input = Input.BoundaryLike
            elif byte == ord('-'):
                input = Input.Dash
            elif byte == ord('\r'):
                input = Input.Cr
            elif byte == ord('\n'):
                input = Input.Lf
            elif byte == ord(':'):
                input = Input.Colon
            elif byte == ord(' '):
                input = Input.Blank
            else:
                input = Input.Alpha

            effect = machine.consume(input)

            if effect == Output.EffectAppendBoundary:
                form_data.boundary += bytes([byte])
            elif effect == Output.EffectAppendData:
                if len(boundary_like) != 0:
                    form_data_part.data = b''.join(
                        [form_data_part.data, boundary_like])
                    boundary_like = bytes()
                form_data_part.data += bytes([byte])
            elif effect == Output.EffectAppendHeader:
                if header_field.decode() == "Content-Disposition":
                    for item in map(lambda s: s.split("=", maxsplit=1), header_value.decode().split("; ")):
                        if len(item) > 1:
                            if item[0] == "name":
                                form_data_part.name = item[1][1:-1]
                            elif item[0] == "filename":
                                form_data_part.filename = item[1][1:-1]
                elif header_field.decode() == "Content-Type":
                    form_data_part.content_type = header_value.decode()
                header_field = bytes()
                header_value = bytes()
            elif effect == Output.EffectAppendHeaderField:
                header_field += bytes([byte])
            elif effect == Output.EffectAppendHeaderValue:
                header_value += bytes([byte])
            elif effect == Output.EffectAppendLikeBoundary:
                boundary_like += bytes([byte])
            elif effect == Output.EffectAppendPart:
                form_data.parts.append(form_data_part)
                form_data_part = FormDataPart()
            elif effect == Output.EffectFormData:
                machine.consume(Input.End)
                return form_data
        return None
