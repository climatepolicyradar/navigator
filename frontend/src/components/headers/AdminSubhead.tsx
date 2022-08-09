interface AdminSubheadProps {
  heading: string;
  description?: string;
}
function AdminSubhead({ heading, description = '' }: AdminSubheadProps) {
  return (
    <div className="border-b border-b-indigo-200 py-6">
      <h3>{heading}</h3>
      {description && (
        <p className="py-4" dangerouslySetInnerHTML={{ __html: description }} />
      )}
    </div>
  );
}
export default AdminSubhead;
