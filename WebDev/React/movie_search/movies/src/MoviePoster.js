import React from 'react';

class MoviePoster extends React.Component {

  constructor(props) {
    super(props)
    this.state = { likes: 0, details: { } }
  }

  getLikeCount = () => {
    fetch(`http://127.0.0.1:5000/likes/${this.props.identifier}`)
      .then((response) => response.json())
      .then((data) => {
        console.log("Got like count", data)
        this.setState({ likes: data['count'] })
      })
  }

  getMovieDetails = () => {
    fetch(this.urlForDetails()).then((response) => response.json()).then((data) => {
      console.log("Got movie details", data)
      this.setState( { details: data })
    })
  }

  componentDidMount() {
    this.getMovieDetails();
    this.getLikeCount()
  }

  incrementLikeCount = (e) => {
    e.preventDefault();
    console.log("Movie", this.props.identifier, "was liked.")

    fetch(`http://127.0.0.1:5000/likes/${this.props.identifier}?change=+1`,
      {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' }
      }
    ).then((response) => response.json())
      .then((data) => {
        this.setState({ likes: data['count'] })
      })
  }

  render = () => {
    const imgUrl = `http://image.tmdb.org/t/p/w185/${this.state.details.poster_path}`
    const altText = `Poster for ${this.state.details.title}`
    return (
      <div className="col-sm-3 text-center mb-2 poster" data-movie-id={this.state.details.id}>
        <img src={imgUrl}
          className="img-fluid"
          alt={altText}>
        </img>
        <p className="mt-2">
          {this.state.details.release_date ? this.state.details.release_date.substr(0, 4) : null}
          <span className="badge bg-primary mx-3">
            {this.state.details.vote_average && this.state.details.vote_average.toFixed(1)}
          </span>
          <a onClick={this.incrementLikeCount} 
            href="#" className="like_button">
            &hearts;
            <span className="like_count">{this.state.likes}</span>
          </a>
        </p>
      </div>
    )
  }

  urlForDetails() {
    const apiKey = "api_key=bde024f3eb43f597aafe01ed9c9098c6"
    const language = "language=en-US"
    const base_url = `https://api.themoviedb.org/3/movie/${this.props.identifier}`
    return `${base_url}?${apiKey}&${language}`
  }

}

export default MoviePoster;
