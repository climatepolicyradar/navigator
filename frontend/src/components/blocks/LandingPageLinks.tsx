import { EyeIcon } from '../Icons';

const LandingPageLinks = ({ handleLinkClick }) => {
  const terms = ['Just transtion', 'Banana', 'Apricot'];
  return (
    <section>
      <div className="md:flex text-white">
        <div className="md:mr-12">
          <EyeIcon />
        </div>
        <div>
          <div className="font-medium text-2xl">Suggested searches</div>
          <ul className="text-lg mt-2">
            {terms.map((term) => (
              <li className="my-2">
                <a
                  className="hover:text-blue-300 transition duration-300"
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
};
export default LandingPageLinks;
