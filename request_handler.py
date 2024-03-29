from http.server import BaseHTTPRequestHandler, HTTPServer
import json

from users import (
    create_user,
    login_user
    )
from categories import (
    get_all_categories,
    get_single_category,
    edit_category,
    create_category,
    delete_category
    )
from posts import (
    get_all_posts,
    edit_post,
    delete_post,
    create_post,
    get_single_post
    )
from tags import (
    get_all_tags,
    get_single_tag,
    create_tag,
    delete_tag,
    edit_tag
)

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
        isLogingIn = None
        
        if self.path == '/login':
            user = login_user(post_body)
            if user:
                response = {
                    'valid': True,
                    'token': user.id
                }
            else:
                response = { 'valid': False }
                
            isLogingIn = True

        if self.path == '/register':
            try:
                new_user = create_user(post_body)
                response = {
                    'valid': True,
                    'token': new_user.id
                }
                self._set_headers(201)
            except Exception as e:
                response = {
                    'valid': False,
                    'error': str(e)
                }
                self._set_headers(400) 
                #400: generic client-side error; 
                #500: generic server-side error;
                #300: redirecting actions;
        
        if self.path == '/categories':
            response = create_category(post_body)
        elif self.path == '/tags':
            response = create_tag(post_body)
        elif self.path == '/posts':
            response = create_post(post_body)
        
        # safe way to set headers for all cases: (instead of setting it at the top)
        if response:
            if isLogingIn:
                if response['valid']:
                    self._set_headers(200)
                else:
                    self._set_headers(404)
            else: 
                self._set_headers(201)
        else:
            self._set_headers(400)

        self.wfile.write(json.dumps(response).encode())  
        
        
    def do_DELETE(self):
        self._set_headers(204)
        (resource, id) = self.parse_url(self.path)
        
        if resource == "categories":
            delete_category(id)
        elif resource == "posts":
            delete_post(id)
        elif resource == "tags":
            delete_tag(id)
            
        self.wfile.write("".encode())
        
        
    def do_PUT(self):
        self._set_headers(204)
        content_len = int(self.headers.get('content-length', 0))
        post_body = self.rfile.read(content_len)
        post_body = json.loads(post_body)

        # Parse the URL
        (resource, id) = self.parse_url(self.path)
        success = False

        if self.path == "/categories":
            response = create_category(post_body)

        if resource == "categories":
            success = edit_category(id, post_body)
            
        elif resource == "posts":
            success = edit_post(id, post_body)
            
        elif resource == "tags":
            success = edit_tag(id, post_body)
            
        if success:
            self._set_headers(204)
        else:
            self._set_headers(404)

        self.wfile.write("".encode())
        

def main():
    host = ''
    port = 8088
    print(f'listening on port {port}!')
    HTTPServer((host, port), RareRequestHandler).serve_forever()


if __name__ == "__main__":
    main()