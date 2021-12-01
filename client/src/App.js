import './App.css';
import TopBar from "./components/TopBar/topbar";
import Home from "./components/home"
import Signup from "./components/SignUp/signup";
import Write from "./components/Write/Write";
import SignIn from "./components/SignIn/signin";
import SideBar from "./components/SideBar/sidebar";
import About from "./components/About/about";
import Profile from "./components/Profile/profile"
import LikedPosts from "./components/LikedPosts/LikedPosts"
import ChangePassword from "./components/ChangePassword/changepassword";
import {
    BrowserRouter as Router,
    Switch,
    Route,

} from "react-router-dom";
import BotBar from "./components/BotBar/botbar";
import MidBar from "./components/MidBar/midBar"
function App() {

    let insertedUser='';
    let insertedPost='';
    return (

    <Router>
        <div className="App">
            <TopBar/>
            <SideBar/>
            <MidBar/>

            <Switch>
                <Route path="/home">
                    <Home/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/profile">
                    <Profile/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/myposts">
                    <LikedPosts/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/changepassword">
                    <ChangePassword/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/login">
                    <SignIn/>

                </Route>
            </Switch>

            <Switch>
                <Route path="/register">
                    <Signup insertedUser={insertedUser}/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/post">
                    <Write insertedPost={insertedPost}/>
                </Route>
            </Switch>
            <Switch>
                <Route path="/about">
                    <About/>
                </Route>
            </Switch>
            <BotBar/>
        </div>
    </Router>
  );
}

export default App;


