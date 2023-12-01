from functools import wraps
from mycrypt import decrypt, encrypt, DATABASE_KEY
from sanic import text, html
import motor

async def check_login(request):
    if request.cookies.get('username') is None:
        return False, "no username"
    if request.cookies.get('password') is None:
        return False, "no password"
    
    client = motor.motor_asyncio.AsyncIOMotorClient('mongodb://172.27.88.132:27017/?replicaSet=rs_noodle')
    users = client['users']
    users_collection = users['users']
    users_doc = await users_collection.find_one({'username': decrypt(request.cookies.get('username'))})
    print(users_doc)
    if users_doc and decrypt(request.cookies.get('password')) == decrypt(users_doc['password'], key=DATABASE_KEY):
        return True, decrypt(request.cookies.get('username'))
    return False, "username or password is wrong"

def protected(wrapped):
    def decorator(f):
        @wraps(f)
        async def decorated_function(request, *args, **kwargs):
            is_authenticated, _ = await check_login(request)

            if is_authenticated:
                response = await f(request, *args, **kwargs)
                return response
            else:
                # 设置延迟时间（以毫秒为单位）
                delay_ms = 5000  # 例如，3秒
                # 设置重定向的目标 URL
                redirect_url = "/signup"
                # 返回包含 JavaScript 的 HTML 响应
                return html(f"""
                <html>
                    <head>
                        <script type="text/javascript">
                            setTimeout(function() {{
                                window.location = '{redirect_url}';
                            }}, {delay_ms});
                        </script>
                    </head>
                    <body>
                        <p>You are unauthorized. You will be redirected in {delay_ms / 1000} seconds.</p>
                    </body>
                </html>
                """, status=401)

        return decorated_function

    return decorator(wrapped)

def add_user_info_cookie(func):
    async def wrapper(request, *args, **kwargs):
        response = await func(request, *args, **kwargs)
        response.cookies['username'] = encrypt(request.args.get('username'))
        response.cookies['password'] = encrypt(request.args.get('password'))
        return response
    return wrapper