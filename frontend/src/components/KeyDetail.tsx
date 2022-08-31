type TProps = {
  detail: string;
  extraDetail?: string;
  amount: number;
  icon?: JSX.Element;
};

export const KeyDetail = ({ detail, amount, icon, extraDetail }: TProps) => {
  return (
    <div className="bg-blue-600 text-white flex h-[90px] items-center justify-center">
      {icon && (
        <div>
          <div className="p-1 bg-white text-blue-600 rounded-full w-[54px] h-[54px] flex items-center justify-center">{icon}</div>
        </div>
      )}
      <div>
        <div className="flex items-center justify-center">
          <div className="text-lg ml-2">{detail}</div>
          <div className="ml-3 text-2xl font-bold drop-shadow-sm">{amount}</div>
        </div>
        <div className="ml-2 text-sm">{extraDetail}</div>
      </div>
    </div>
  );
};
