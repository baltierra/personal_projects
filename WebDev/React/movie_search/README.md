# Week 8

Today we'll finish our tour of React by combining it with a Python service.

We will also learn about browser 'cookies' to see how they help with state management.

### If You Want To Code Along

After cloning the repository, you'll need to prepare the `movies` application: 

```
week8        $ cd movies
week8/movies $ npm install
```

Now you can start the movies app:

```
week8/movies $ npm start
```


Next, in a NEW terminal/shell tab or window, install a Python module:

```
week8        $ cd server
week8/server $ pip3 install flask-cors
```

and then start the Python service:

``` 
week7/server $ flask --app server --debug run
````

You can open its home page at [127.0.0.1:5000](http://127.0.0.1:5000) in your browser.

When you're done, use CTRL-C on BOTH servers to shut everything down.

## Agenda 

1. New code architecture: MoviePosters now have state!
2. Implementing HTML forms in React
3. React: OOP or Functional?
4. Using an external Python service to manage 'Like' state for each movie
5. HTTP is stateless, so we how can we maintain state across page refreshes?
6. One last word about frameworks
7. Thought experiment: How would we all share the same movie data (i.e. 'like' counts) amongst ourselves?
8. What haven't we done?

