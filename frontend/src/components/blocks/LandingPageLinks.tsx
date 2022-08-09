import { EyeIcon } from '../svg/Icons';

function LandingPageLinks({ handleLinkClick }) {
  const terms = [
    'Adaptation strategy',
    'Energy prices',
    'Flood defence',
    'Just transition',
  ];
  return (
    <section>
      <div className="md:flex text-white">
        <div className="md:mr-12">
          <EyeIcon />
        </div>
        <div>
          <div className="font-medium text-2xl">Suggested searches</div>
          <ul className="text-lg mt-4">
            {terms.map((term) => (
              <li className="my-2" key={term}>
                <a
                  className="hover:text-blue-500 transition duration-300"
                  href="/"
                  onClick={(e) => {
                    handleLinkClick(e);
                  }}
                >
                  {term}
                </a>
              </li>
            ))}
          </ul>
        </div>
      </div>
    </section>
  );
}
export default LandingPageLinks;
