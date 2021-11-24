from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from users import create_user, login_user

from posts import get_all_posts, edit_post, delete_post

from categories import get_all_categories

from comments import get_all_comments, get_single_comment, create_comment


class RareRequestHandler(BaseHTTPRequestHandler):

    def _set_headers(self, status):
        self.send_response(status)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE')
        self.send_header('Access-Control-Allow-Headers', 'X-Requested-With, Content-Type, Accept')
        self.end_headers()

    def parse_url(self, path):
        path_params = path.split("/")
        resource = path_params[1]

        # Check if there is a query string parameter
        if "?" in resource:
            # GIVEN: /customers?email=jenna@solis.com

            param = resource.split("?")[1]  # email=jenna@solis.com
            resource = resource.split("?")[0]  # 'customers'
            pair = param.split("=")  # [ 'email', 'jenna@solis.com' ]
            key = pair[0]  # 'email'
            value = pair[1]  # 'jenna@solis.com'

            return ( resource, key, value )

        # No query string parameter
        else:
            id = None

            try:
                id = int(path_params[2])
            except IndexError:
                pass  # No route parameter exists: /animals
            except ValueError:
                pass  # Request had trailing slash: /animals/

            return (resource, id)


    def do_GET(self):
        self._set_headers(200)
        
        response = {}
        
        parsed = self.parse_url(self.path)
        
        if len(parsed) == 2:
            ( resource, id ) = parsed
        
            if resource == "users":
                if id is not None:
                    response = f"{get_single_user(id)}"
                else:
                    response = f"{get_all_users()}"
            elif resource == "posts":
                if id is not None:
                    response = f"{get_single_post(id)}"
                else:
                    response = f"{get_all_posts()}"
            elif resource == "comments":
                if id is not None:
                    response = f"{get_single_comment(id)}"
                else:
                    response = f"{get_all_comments()}"
            elif resource == "categories":
                if id is not None:
                    response = f"{get_single_category(id)}"
                else:
                    response = f"{get_all_categories()}"
            elif resource == "subscriptions":
                if id is not None:
                    response = f"{get_single_subscription(id)}"
                else:
                    response = f"{get_all_subscriptions()}"
           
            elif resource == "post_tags":
                if id is not None:
                    response = f"{get_single_post_tag(id)}"
                else:
                    response = f"{get_all_post_tags()}"
            elif resource == "tags":
                if id is not None:
                    response = f"{get_single_tag(id)}"
                else:
                    response = f"{get_all_tags()}"
            elif resource == "post_reactions":
                if id is not None:
                    response = f"{get_single_post_reaction(id)}"
                else:
                    response = f"{get_all_post_reactions()}"
            elif resource == "reactions":
                if id is not None:
                    response = f"{get_single_reaction(id)}"
                else:
                    response = f"{get_all_reactions()}"
                    
            elif len (parsed) == 3:
            ( resource, key, value ) = parsed
            
        self.wfile.write(response.encode())
    
    
    def do_POST(self):
        content_len = int(self.headers.get('content-length', 0))
        raw_body = self.rfile.read(content_len)
        post_body = json.loads(raw_body)

        response = None
        
        if self.path == '/login':
            user = login_user(post_body)
            if user:
                response = {
                    'valid': True,
                    'token': user.id
                }
                self._set_headers(200)
            else:
                response = { 'valid': False }
                self._set_headers(404)

        if self.path == '/register':
            try:
                new_user = create_user(post_body)
                response = {
                    'valid': True,
                    'token': new_user.id
                }
            except Exception as e:
                response = {
                    'valid': False,
                    'error': str(e)
                }
                
        if self.path == '/comments':
            new_comment = create_comment(post_body)
            if new_comment:
                response = {
                    'valid': True,
                    'token': new_comment.id
                }
            
            self._set_headers(201)

        self.wfile.write(json.dumps(response).encode())

    def do_PUT(self):
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        (resource, id) = self.parse_url(self.path)
        success = False
        if resource == "posts":
            success = edit_post(id, post_body)
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)
            
        self.wfile.write("".encode())

        
    def do_DELETE(self):
        # Set a 204 response code
        self._set_headers(204)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)

        if resource == "posts":
            delete_post(id)

        # Encode the new post and send in response
        self.wfile.write("".encode())

def main():
    host = ''
    port = 8088
    print(f'listening on port {port}!')
    HTTPServer((host, port), RareRequestHandler).serve_forever()


if __name__ == "__main__":
    main()