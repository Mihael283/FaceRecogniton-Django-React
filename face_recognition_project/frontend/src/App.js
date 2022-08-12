import { Container } from 'react-bootstrap'
import RegisterScreen from './screens/RegisterScreen'

import { BrowserRouter as Router, Route , Routes} from 'react-router-dom'




function App() {
  return (
    <Router>  
        <main className = "py-3">
          <Container>
            <Routes>
              
              <Route path="/register" element ={ <RegisterScreen/>}/>
            </Routes>
          </Container>
        </main>
        
    </Router>
    
  );
}


export default App;
