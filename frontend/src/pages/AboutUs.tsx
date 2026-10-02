import "./AboutUs.css";

function AboutUs() {
  return (
    <div className="page">
      <img
        src="/simpsons.gif"
        alt="Mr. Burns on a tightrope: So, I see by your tie you're a Yale man, too."
        className="about-us-gif"
      />
      <h1 className="wordart-text">About Us</h1>
      <p className="wordart-text">
        We are the home of letting everyone else know that you chose your
        school for it's likelihood of turning you into another coastal elite.
        The best thing about a ball cap with a Y on it is that people will
        immediately think you're much smart than them, or so you think, and
        that's why you buy them.
      </p>
    </div>
  );
}

export default AboutUs;
