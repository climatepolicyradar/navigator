import { useEffect, useRef, useCallback } from "react";
import { addClass, removeClass } from "@utils/cssClass";

const SuggestList = ({ list, setList, keyField, keyFieldDisplay, type, setInput, handleFilterChange }) => {
  const ulRef = useRef(null);
  let liSelected;
  let index = -1;

  const navigateList = useCallback(
    (e): void => {
      const ul = ulRef.current;
      const len = list.length - 1;

      if (e.key === "ArrowDown") {
        // eslint-disable-next-line react-hooks/exhaustive-deps
        index += 1;
        // down
        if (liSelected) {
          removeClass(liSelected, "selected");
          let next = ul.getElementsByTagName("li")[index];
          if (typeof next !== undefined && index <= len) {
            // eslint-disable-next-line react-hooks/exhaustive-deps
            liSelected = next;
          } else {
            index = 0;
            liSelected = ul.getElementsByTagName("li")[0];
          }
          addClass(liSelected, "selected");
        } else {
          index = 0;
          liSelected = ul.getElementsByTagName("li")[0];
          addClass(liSelected, "selected");
        }
      } else if (e.key === "ArrowUp") {
        // up
        if (liSelected) {
          removeClass(liSelected, "selected");
          index -= 1;
          let next = ul.getElementsByTagName("li")[index];
          if (typeof next !== undefined && index >= 0) {
            liSelected = next;
          } else {
            index = len;
            liSelected = ul.getElementsByTagName("li")[len];
          }
          addClass(liSelected, "selected");
        } else {
          index = 0;
          liSelected = ul.getElementsByTagName("li")[len];
          addClass(liSelected, "selected");
        }
      } else if (e.key === "Enter") {
        if (liSelected) {
          liSelected.click();
          window.removeEventListener("keydown", navigateList);
        }
      }
    },
    [liSelected, index, list]
  );

  const handleClick = (item) => {
    handleFilterChange(type, item[keyField]);
    setList([]);
    setInput("");
    liSelected = null;
    index = -1;
  };

  useEffect(() => {
    if (list.length) {
      window.addEventListener("keydown", navigateList);
    } else {
      window.removeEventListener("keydown", navigateList);
    }

    return () => {
      window.removeEventListener("keydown", navigateList);
    };
  }, [list, navigateList]);

  return (
    <ul ref={ulRef} className="bg-white rounded-b-lg border-t-dotted border-b border-l border-r">
      {list.map(
        (item, index) =>
          index < 10 && (
            <li
              key={index}
              onClick={() => {
                handleClick(item);
              }}
              className="hover:bg-blue-200 cursor-pointer my-1 p-2"
            >
              {item[keyFieldDisplay ?? keyField]}
            </li>
          )
      )}
    </ul>
  );
};

export default SuggestList;
