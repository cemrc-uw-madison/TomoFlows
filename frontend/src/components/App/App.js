import React, {useState, useEffect} from "react";
import "./App.css"

const App = (props) => {
	const [res, setRes] = useState()
	
	useEffect(() => {
		fetch("/api/ping")
			.then(response => response.json())
			.then(data => setRes(data.message))
			.catch(err => console.log(err))
	}, [])
	return (
		<div className="App">
			<h1>TomoFlows</h1>
			<p><b>API Ping: </b> {res ?? "Loading..."}</p>
		</div>
	);
};

export default App;
