from flask import Flask, render_template, request, redirect, url_for, session

app = Flask(__name__)
app.secret_key = 'supersecretkey'

@app.before_request
def init_session():
    if 'productos' not in session:
        session['productos'] = []

@app.route('/')
def index():
    return render_template('index.html', productos=session['productos'])

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_producto():
    if request.method == 'POST':
        nuevo_producto = {
            'id': request.form['id'],
            'nombre': request.form['nombre'],
            'cantidad': request.form['cantidad'],
            'precio': request.form['precio'],
            'fecha_ven': request.form['fecha_ven'],
            'categoria': request.form['categoria']
        }
        for producto in session['productos']:
            if producto['id'] == nuevo_producto['id']:
                return "------El ID del producto ya existe, prueba con otro ID------"

        session['productos'].append(nuevo_producto)
        session.modified = True
        return redirect(url_for('index'))
    return render_template('agregar.html')

@app.route('/eliminar/<string:id>')
def eliminar_producto(id):
    session['productos'] = [p for p in session['productos'] if p['id'] != id]
    session.modified = True
    return redirect(url_for('index'))

@app.route('/editar/<string:id>', methods=['GET', 'POST'])
def editar_producto(id):
    producto = next((p for p in session['productos'] if p['id'] == id), None)
    if request.method == 'POST':
        if producto:
            producto['nombre'] = request.form['nombre']
            producto['cantidad'] = request.form['cantidad']
            producto['precio'] = request.form['precio']
            producto['fecha_ven'] = request.form['fecha_ven']
            producto['categoria'] = request.form['categoria']
            session.modified = True
        return redirect(url_for('index'))
    return render_template('editar.html', producto=producto)

if __name__ == '__main__':
    app.run(debug=True)