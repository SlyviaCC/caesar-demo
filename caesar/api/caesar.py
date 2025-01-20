import json

alphabet = [
    'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
    'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w',
    'x', 'y', 'z'
]

def caesar(original_text, shift_amount, encode_or_decode):
    output_text = ""
    # decode时，shift取负数
    if encode_or_decode == "decode":
        shift_amount *= -1

    for letter in original_text:
        if letter not in alphabet:
            output_text += letter
        else:
            shifted_position = alphabet.index(letter) + shift_amount
            # 为了避免超出范围，用模运算
            shifted_position %= len(alphabet)
            output_text += alphabet[shifted_position]
    return output_text


def handler(request):
    """
    Vercel Serverless Function 入口函数。
    接收 POST 请求，对请求体中的 text, shift, direction (encode/decode) 进行处理并返回结果。
    """
    # 只允许 POST
    if request.method != "POST":
        return {
            "statusCode": 405,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": "Method Not Allowed. Please use POST."})
        }

    try:
        # 从请求的 JSON body 中获取参数
        body = request.get_json()
        direction = body.get("direction", "encode")
        text = body.get("text", "")
        shift = int(body.get("shift", 3))

        # 调用加解密函数
        result_text = caesar(
            original_text=text,
            shift_amount=shift,
            encode_or_decode=direction
        )

        # 返回结果
        return {
            "statusCode": 200,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({
                "message": f"Here is the {direction}d result",
                "result": result_text
            })
        }
    except Exception as e:
        return {
            "statusCode": 400,
            "headers": { "Content-Type": "application/json" },
            "body": json.dumps({"error": str(e)})
        }