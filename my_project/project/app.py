from flask import render_template, request, redirect
import parcer
import models

app = models.app
req = ''
cnt_get = None


@app.route('/index')
@app.route('/')
def index():
    return render_template('index.html'), 200


@app.route('/gettoys')
def gettoys():
    gettoys = models.db.session.query(models.Post).order_by(models.Post.id.desc()).limit(cnt_get).all()
    gettoys.reverse()
    title = req
    return render_template('gettoys.html', gettoys=gettoys, title=title), 200

@app.route('/myrequest', methods=['POST', 'GET'])
def myrequest():
    if request.method == 'POST':
        global req
        req = request.form['title']
        start_parser = parcer.parcer_start(req)
        data = start_parser[0]
        global cnt_get
        cnt_get = start_parser[1]
        for page in data:
            post = models.Post(title=page.get('title'),
                        brand_name=page.get('brand_name'),
                        url=page.get('url'))
            try:
                models.db.session.add(post)
                models.db.session.commit()
            except:
                return 'При добавлении данных в бд произошла ошибка'
        return redirect('/gettoys')
    else:
        return render_template('myrequest.html'), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001, debug=True)