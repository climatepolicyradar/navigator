import { HERO_DEFAULT_HEIGHT } from '@constants/hero';

type TProps = {
  height?: number;
};

function FullHeight({ height = HERO_DEFAULT_HEIGHT }: TProps) {
  return (
    <div
      className="banner banner--full h-screen overflow-hidden"
      style={{ minHeight: height }}
    />
  );
}

export default FullHeight;
