from micronic import Micronic, Response, Rule, render_template

app = Micronic()

def a_handler(request):
    return render_template('hello.html', {'foo': 'bar'})

@app.route('/')
def and_another_handler(request):
    return Response("From and_another_handler")


app.add_route(Rule('/a', endpoint=a_handler))



app.run()
app.serve(debug=True, use_reloader=True)
