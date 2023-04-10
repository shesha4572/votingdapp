import {Register} from "./components/Register";
import ReactDOM from "react-dom/client";
import {Login} from "./components/Login";
import {BrowserRouter, Route, Routes} from "react-router-dom";
import {AdminLogin} from "./components/Admin-Login";
import {Homepage} from "./components/homepage";
import {Voting} from "./components/Voting";
import {Result} from "./components/Result";
function App() {
  return (
    <div id="App">
    <BrowserRouter>
      <Routes>
        <Route path={"/voterLogin"} element={<Login/>}/>
        <Route path={"/voterRegister"} element={<Register/>}/>
        <Route path={"/adminLogin"} element={<AdminLogin/>}/>
        <Route path={"/"} element={<Homepage/>}/>
        <Route path={"/vote"} element={<Voting/>}/>
        <Route path={"/result"} element={<Result/>}/>
      </Routes>
    </BrowserRouter>
    </div>
  )
}
export default App;
