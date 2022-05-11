import Image from 'next/image';

const Partners = () => {
  return (
    <div className="py-24">
      <div className="max-w-screen-lg mx-auto">
        <h2 className="text-indigo-500 mb-8">Our Partners</h2>
        <div>
          <a href="/">
            <Image
              src="/images/partners/lse-logo.png"
              alt="LSE"
              width="235"
              height="240"
            />
          </a>
        </div>
      </div>
    </div>
  );
};
export default Partners;
