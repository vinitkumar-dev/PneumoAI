// Home.jsx
import Navbar from "../../components/Navbar/Navbar";
import Hero from "../../components/Hero/Hero";
import Features from "../../components/Features/Features";
// import Statistics from "../../components/Statistics/Statistics";
// import About from "../../components/About/About";
import CTA from "../../components/CTA/CTA";
import Footer from "../../components/Footer/Footer";
import "./Home.css";

function Home() {
  return (
    <div className="landing-page-root">
      <Navbar />

      {/* Semantic landmark containers mapping structural presentation contexts */}
      <main id="main-content" className="landing-viewport-flow">
        <Hero />
        <Features />
        {/* <Statistics /> */}
        {/* <About /> */}
        <CTA />
      </main>

      <Footer />
    </div>
  );
}

export default Home;
