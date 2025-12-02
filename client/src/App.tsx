import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import {GreetingPage} from "./pages/GreetingPage/GreetingPage.tsx";
import {AnalysisPage} from "./pages/AnalysisPage/AnalysisPage.tsx";

function App() {



  return (
    <>
        <Router>
            <Routes>
                <Route path="/"  element={<GreetingPage />}/>
                <Route path="/analysis" element={<AnalysisPage />}/>
            </Routes>
        </Router>
    </>
  )
}

export default App
