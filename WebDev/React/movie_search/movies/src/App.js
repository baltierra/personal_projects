import React from 'react';
import MoviePoster from './MoviePoster'

class App extends React.Component {

  constructor(props) {
    super(props)
    this.state = {
      movies: [],
      likes: { },
      searchTerm: ""
    }
  }

  showOurTop10 = async (e) => {
    fetch(`http://127.0.0.1:5000/likes/top10`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Got top 10", data)
        const movie_objects = data.map(movie_id => { return {id: movie_id} })
        this.setState({ movies: movie_objects })
      })
  }

  showNowPlaying = async (e) => {
    const url = this.urlForMovies("now_playing")
    const httpResponse = await fetch(url)
    const data = await httpResponse.json()
    console.log(data)
    this.setState({ movies: data.results.filter(movie => movie.vote_average > 7.0) })
  }

  showTopRatedMovies = async (e) => {
    const url = this.urlForMovies("top_rated")
    const httpResponse = await fetch(url)
    const data = await httpResponse.json()
    console.log(data)
    this.setState( { movies: data.results.filter(movie => movie.vote_average > 7.0) } )
  }

  handleSearchTermChange = (e) => {
    this.setState( { searchTerm: e.target.value })
  }

  performSearch = async (e) => {
    e.preventDefault()
    console.log("Form submitted!")
    // document.querySelector
    const url = this.urlForSearch(this.state.searchTerm)
    const httpResponse = await fetch(url)
    const data = await httpResponse.json()
    this.setState({ searchTerm: "", movies: data.results.filter(movie => (movie.vote_average > 7.0))})
  }

  render() {
    const posters = this.state.movies.map(movie_data => {
      return (
        <MoviePoster identifier={movie_data.id} key={movie_data.id}/>
      )
    })
    return (
      <div>
        <header className="row mb-5 justify-content-between">
          <form onSubmit={this.performSearch} className="col-sm-4">
            <input value={this.state.searchTerm} onChange={this.handleSearchTermChange} className="form-control" autoFocus name="search" type="text" placeholder="Search by title...">
            </input>
          </form>

          <p className="mt-2">
            <button onClick={this.showTopRatedMovies} className="btn btn-primary" >Top-Rated Movies</button>
            <button onClick={this.showNowPlaying} className="btn btn-primary ms-3">Now Playing</button>
            <button onClick={this.showOurTop10} className="btn btn-primary ms-3">Our Top 10</button>
          </p>
        </header>

        <div className="row" id="movies"> 
          { posters }
        </div>
      </div>
    )
  }

  urlForSearch(keyword) {
    const apiKey = "api_key=bde024f3eb43f597aafe01ed9c9098c6"
    const language = "language=en-US"
    const region = "region=US"
    const filter = "include_adult=false"
    const query = "query=" + keyword
    const base_url = `https://api.themoviedb.org/3/search/movie`
    return `${base_url}?${apiKey}&${language}&${region}&${filter}&${query}`
  }
  urlForMovies(resource) {
    const apiKey = "api_key=bde024f3eb43f597aafe01ed9c9098c6"
    const language = "language=en-US"
    const region = "region=US"
    const filter = "include_adult=false"
    const base_url = `https://api.themoviedb.org/3/movie/${resource}`
    return `${base_url}?${apiKey}&${language}&${region}&${filter}`
  }

}

export default App;
