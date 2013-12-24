from micronic import Micronic, Response, render_template

app = Micronic()

def a_handler(request):
    return render_template('hello.html', {'foo': 'bar'})

@app.route('/')
def and_another_handler(request):
    return Response("From and_another_handler")


app.add_route(('/a', a_handler))


app.serve(debug=True, use_reloader=True)
