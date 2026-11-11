import { Routes, Route, Link } from "react-router"
import RegisterPackagePage from './pages/RegisterPackagePage.jsx'
import PackageDetailPage from './pages/PackageDetailPage.jsx'

function App() {
  return (
    <>
      <nav>
        <Link to="/">Register Package</Link>
      </nav>
      <Routes>
        <Route path="/" element={<RegisterPackagePage />} />
        <Route path="/packages/:id" element={<PackageDetailPage />} />
        <Route path="*" element={<h1>404 Not Found</h1>} />
      </Routes>
    </>
  )
}

export default App