
export const getDocumentTitle = (name: string, postfix: string) => {
  return postfix ? `${name} [${postfix}]` : name;
};
