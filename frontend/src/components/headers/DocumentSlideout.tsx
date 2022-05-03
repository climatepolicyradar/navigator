import ToggleDocumentMenu from '../menus/ToggleDocumentMenu';

const DocumentSlideout = ({ name, length, showPDF, setShowPDF }) => {
  return (
    <div className="border-b border-blue-200 pb-4 flex justify-between relative">
      <div className="pl-6 pr-10 mt-2">
        <h1 className="text-lg text-blue-500 font-medium">{name}</h1>
        {/* TODO: translate below text, how to handle plurals? */}
        <p className="text-indigo-500 text-sm">
          {length} {`match${length === 1 ? '' : 'es'}`} in document.
        </p>
      </div>
      <ToggleDocumentMenu setShowPDF={setShowPDF} showPDF={showPDF} />
    </div>
  );
};
export default DocumentSlideout;
