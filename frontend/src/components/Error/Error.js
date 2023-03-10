import React from "react"
import "./Error.css"

const Error = (props) => {
  return (
    <div className="Error">
      <h1>Oops!</h1>
      <p>Sorry, an unexpected error has occurred.</p>
      <p>
        <i>Page Not Found</i>
      </p>
    </div>
  );
}

export default Error
