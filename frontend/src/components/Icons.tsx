interface IconProps {
  width?: string;
  height?: string;
  color?: string;
}
export function CloseIcon({
  width,
  height,
  color = 'currentColor',
}: IconProps) {
  return (
    <svg
      style={{ width: `${width}px`, height: `${height}px` }}
      version="1.1"
      id="Capa_1"
      fill={color}
      xmlns="http://www.w3.org/2000/svg"
      x="0px"
      y="0px"
      viewBox="0 0 341.751 341.751"
    >
      <g>
        <g>
          <rect
            x="-49.415"
            y="149.542"
            transform="matrix(0.7072 -0.707 0.707 0.7072 -70.7868 170.8326)"
            width="440.528"
            height="42.667"
          />
        </g>
      </g>
      <g>
        <g>
          <rect
            x="149.569"
            y="-49.388"
            transform="matrix(0.707 -0.7072 0.7072 0.707 -70.7712 170.919)"
            width="42.667"
            height="440.528"
          />
        </g>
      </g>
    </svg>
  );
}
