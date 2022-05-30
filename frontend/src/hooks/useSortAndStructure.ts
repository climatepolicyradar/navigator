import { sortData } from '../utils/sorting';
import { removeDuplicates } from '../utils/removeDuplicates';

const useSortAndStructure = () => {
  const extractParentLevel = (data) => {
    const level = data.map((item) => {
      const splitName = item.name.split('|');
      return { name: splitName[1] };
    });
    const unDuped = removeDuplicates(level, 'name');
    return sortData(unDuped, 'name');
  };
  const extractChildLevel = (data) => {
    const level = data.map((item) => {
      const splitName = item.name.split('|');
      return { parent: splitName[1], name: splitName[0] };
    });
    return sortData(level, 'name');
  };

  const buildNewData = (parentLevel, childLevel) => {
    const newData = parentLevel.map((parent) => {
      const children = childLevel.filter(
        (child) => child.parent === parent.name
      );
      const obj = { name: parent.name, children };
      return obj;
    });
    return newData;
  };

  const structureData = (data) => {
    const parentLevel = extractParentLevel(data);
    const childLevel = extractChildLevel(data);
    return buildNewData(parentLevel, childLevel);
  };
  return structureData;
};
export default useSortAndStructure;
