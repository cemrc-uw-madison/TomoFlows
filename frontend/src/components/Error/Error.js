import React from "react"
import "./Error.css"

/**
 * Error page to provide for a good user experience when bugs or problems
 * are encountered by the user
 * @param {*} props - properties passed in from parent component
 * @returns JSX
 */
const Error = (props) => {
	return (
		<div className="Error">
			<h2>Oops!</h2>
			<p>Sorry, an unexpected error has occurred.</p>
			<p>
				<i>Page Not Found</i>
			</p>
		</div>
	);
}

export default Error
