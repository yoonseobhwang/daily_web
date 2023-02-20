from flask import Flask, request, redirect

app = Flask(__name__)

topics = [
    {'id':1, 'title': 'html', 'body': 'html is ...'},
    {'id':2, 'title': 'css', 'body': 'css is ...'},
    {'id':3, 'title': 'javascript', 'body': 'javascript is ...'}
]
nextid = max([topic['id'] for topic in topics]) + 1 

def template(contents, content, id=None):
    contextUI = ''
    if id:
        contextUI = f'''
        <li><a href="/update/{id}/">update</a></li>
        <li><form action="/delete/{id}" method="POST"><input type="submit" value="delete"></form></li>
        '''
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
                {contextUI}
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
            title, body = topic['title'], topic['body']
            break
    
    return template(get_Contents(), f'<h2>{title}</h2>{body}', id)

@app.route('/create/', methods=['GET', 'POST'])
def create():
    req = request.method
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
    
    
@app.route('/update/<int:id>/', methods=['GET','POST']) 
def update(id):
    req = request.method

    if req == 'GET':
        for topic in topics:
            if id == topic['id']:
                title, body = topic['title'], topic['body']
                break    
        content = f'''
            <form action="/update/{id}/" method="POST">
                <p><input type="text" name='name' placeholder="title", value="{title}"></p>
                <p><textarea name='body' placeholder="body">{body}</textarea></p>
                <p><input type="submit" value="update"></p>
        '''
        return template(get_Contents(), content)

    else:
        title = request.form['name']
        body = request.form['body']
        newtopic = {'id':id, 'title':title, 'body':body}
        for idx, topic in enumerate(topics):
            if topic['id'] == id:
                topics[idx] = newtopic
                break

        url = '/read/' + str(id)
        return redirect(url)

@app.route('/delete/<int:id>/', methods=['POST'])
def delete(id):
    for topic in topics:
        if topic['id'] == id:
            topics.remove(topic)
            break

    return redirect('/')

if __name__ == "__main__":
    app.run(debug=True)