import * as React from 'react';

import { User } from '../interfaces';

type ListDetailProps = {
  item: User;
};

function ListDetail({ item: user }: ListDetailProps) {
  return (
    <div>
      <h1>Detail for{user.name}</h1>
      <p>ID:{user.id}</p>
    </div>
  );
}

export default ListDetail;
