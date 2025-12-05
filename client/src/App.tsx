import './App.css'
import {BrowserRouter as Router, Routes, Route} from "react-router-dom";
import {GreetingPage} from "./pages/GreetingPage/GreetingPage.tsx";
import {AnalysisPage} from "./pages/AnalysisPage/AnalysisPage.tsx";
import {StatisticsPage} from "./pages/StatisticsPage/StatisticsPage.tsx";

function App() {



  return (
    <>
        <Router>
            <Routes>
                <Route path="/"  element={<GreetingPage />}/>
                <Route path="/analysis" element={<AnalysisPage />}/>
                <Route path="/statistics" element={<StatisticsPage />}/>
            </Routes>
        </Router>
    </>
  )
}

export default App
