from flask import Flask, request, redirect

app = Flask(__name__)

topics = [
    {'id':1, 'title': 'html', 'body': 'html is ...'},
    {'id':2, 'title': 'css', 'body': 'css is ...'},
    {'id':3, 'title': 'javascript', 'body': 'javascript is ...'}
]
nextid = max([topic['id'] for topic in topics]) + 1 

def template(contents, content):
    return f'''<!doctype html>
    <html>
        <body>
            <h1><a href="/">WEB</a></h1>
            <ol>
                {contents}
            </ol>
                {content}
            <ul>
                <li><a href="/create/">create</a></li>
        </body>
    </html>
    '''

def get_Contents():
    liTags = ''
    for topic in topics:
        liTags = liTags + f'<li><a href="/read/{topic["id"]}/">{topic["title"]}</a></li>'
    return liTags

@app.route('/')
def home():
    return template(get_Contents(), '<h2>WELCOME</h2>Hello, WEB')


@app.route('/read/<int:id>/')
def read(id):
    for topic in topics:
        if id == topic['id']:
            title, body = topic['body'], topic['body']
            break
    
    return template(get_Contents(), f'<h2>{title}</h2>{body}')

@app.route('/create/', methods=['GET', 'POST'])
def create():
    req = request.method
    print(req)
    if req == 'GET':    
        content = '''
            <form action="/create/" method="POST">
                <p><input type="text" name='name' placeholder="title"></p>
                <p><textarea name='body' placeholder="body"></textarea></p>
                <p><input type="submit" value="create"></p>
        '''
        return template(get_Contents(), content)

    else:
        global nextid
        title = request.form['name']
        body = request.form['body']
        newtopic = {'id':nextid, 'title':title, 'body':body}
        topics.append(newtopic)
        url = '/read/' + str(nextid)
        print(url)
        nextid += 1 
        return redirect(url)

if __name__ == "__main__":
    app.run(debug=True)