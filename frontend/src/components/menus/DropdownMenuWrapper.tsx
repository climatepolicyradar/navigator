import React from 'react';
interface DropdownMenuWrapperProps {
  children: React.ReactNode;
  setShowMenu(value: boolean): void;
}
const DropdownMenuWrapper = ({
  children,
  setShowMenu,
}: DropdownMenuWrapperProps) => {
  const childrenWithProps = React.Children.map(children, (child) => {
    // Checking isValidElement is the safe way and avoids a typescript
    // error too.
    if (React.isValidElement(child)) {
      return React.cloneElement(child, { setShowMenu });
    }
    return child;
  });
  return (
    <div
      data-cy="dropdown-menu"
      className="rounded bg-indigo-100 shadow-xl shadow-black/10 py-2 w-48"
    >
      {childrenWithProps}
    </div>
  );
};
export default DropdownMenuWrapper;
