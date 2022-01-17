interface LogoProps {
  fixed: boolean;
}

const Logo = ({ fixed }: LogoProps) => {
  return (
    <svg
      fill="none"
      xmlns="http://www.w3.org/2000/svg"
      viewBox="0 0 113 60"
      width={fixed ? '75' : '113'}
      height={fixed ? '40' : '60'}
      className="transition-all duration-300"
    >
      <path
        fill="currentColor"
        d="M46.15 16.777c-2.268 0-4.126-.785-5.577-2.358-1.45-1.57-2.173-3.566-2.173-5.986 0-2.433.704-4.449 2.117-6.042C41.93.8 43.803 0 46.131 0c1.924 0 3.464.507 4.628 1.522 1.164 1.015 1.835 2.321 2.018 3.914h-3.243c-.15-.827-.521-1.48-1.117-1.964-.592-.48-1.357-.724-2.286-.724-1.427 0-2.516.527-3.267 1.579-.751 1.052-1.127 2.42-1.127 4.106 0 1.668.404 3.03 1.207 4.083.802 1.052 1.872 1.579 3.21 1.579.948 0 1.737-.259 2.366-.78.629-.517 1-1.208 1.103-2.063h3.201c-.089 1.518-.685 2.79-1.779 3.81-1.22 1.147-2.849 1.715-4.895 1.715Zm8.157-.337V.314h3.065V16.44h-3.065ZM59.4 3.068V.315h3.065v2.753H59.4Zm0 13.371V4.872h3.065V16.44H59.4Zm5.046 0V4.872h2.952v1.555h.066c.737-1.25 1.854-1.87 3.356-1.87.723 0 1.361.184 1.924.555.564.37.986.86 1.272 1.475h.047c.84-1.353 2-2.03 3.47-2.03 1.2 0 2.135.367 2.806 1.095.666.728 1.005 1.734 1.005 3.012v7.78h-3.066V9.18c0-1.325-.591-1.982-1.779-1.982-.647 0-1.154.23-1.52.686-.366.46-.554 1.07-.554 1.837v6.718H71.36V9.18c0-1.325-.592-1.982-1.78-1.982-.614 0-1.116.23-1.496.686-.385.46-.573 1.07-.573 1.837v6.718h-3.065Zm26.069.001c-.15-.198-.272-.626-.361-1.288h-.047a3.41 3.41 0 0 1-1.263 1.15c-.511.273-1.225.405-2.14.405-1.216 0-2.192-.31-2.93-.926-.736-.615-1.102-1.489-1.102-2.616 0-1.175.404-2.035 1.216-2.584.812-.55 1.952-.93 3.426-1.137 1.08-.15 1.817-.306 2.206-.46.39-.16.587-.442.587-.846 0-.423-.164-.757-.498-1.006-.333-.249-.812-.371-1.44-.371-1.4 0-2.141.54-2.23 1.626h-2.727c.047-1.1.488-2.007 1.328-2.73.84-.724 2.056-1.08 3.652-1.08 3.243 0 4.867 1.418 4.867 4.26v5.887c0 .874.136 1.405.404 1.602v.113h-2.948Zm-3.065-1.87c.84 0 1.507-.217 1.995-.654.488-.437.732-.954.732-1.555v-1.738c-.328.197-1.042.423-2.14.676-.873.198-1.488.418-1.85.668-.36.248-.54.63-.54 1.136 0 .978.602 1.466 1.803 1.466Zm6.647-7.669v-2.03h1.6V1.263h2.995v3.608h1.981v2.03h-1.981v6.136c0 .766.385 1.15 1.15 1.15l.901-.023v2.256a33.06 33.06 0 0 1-1.915.046c-.887 0-1.629-.216-2.23-.643-.6-.428-.9-1.137-.9-2.133V6.9h-1.601Zm13.471 9.876c-1.863 0-3.328-.573-4.393-1.724-1.066-1.151-1.601-2.622-1.601-4.407 0-1.729.535-3.176 1.601-4.341 1.065-1.165 2.431-1.748 4.102-1.748 1.817 0 3.22.63 4.215 1.894.991 1.263 1.488 2.955 1.488 5.074h-8.383c.117.916.427 1.625.925 2.133.497.502 1.173.756 2.027.756 1.127 0 1.869-.474 2.23-1.419h3.018c-.225 1.08-.798 1.983-1.713 2.706-.915.724-2.089 1.076-3.516 1.076Zm-.249-9.852c-1.488 0-2.379.827-2.68 2.48h5.135c-.047-.737-.291-1.333-.741-1.794-.451-.46-1.019-.686-1.714-.686ZM39.1 38.05V21.928h7.073c1.83 0 3.239.502 4.215 1.512.962.992 1.441 2.218 1.441 3.674 0 1.532-.479 2.768-1.44 3.698-.963.935-2.277 1.4-3.944 1.4H42.48v5.84H39.1Zm3.38-13.281v4.783h3.379c.84 0 1.488-.216 1.938-.644.45-.427.676-1.02.676-1.771 0-.752-.225-1.334-.676-1.748-.45-.413-1.08-.62-1.891-.62h-3.427ZM62.69 36.64c-1.126 1.166-2.576 1.749-4.346 1.749-1.774 0-3.22-.583-4.346-1.748-1.127-1.165-1.69-2.622-1.69-4.365 0-1.743.563-3.2 1.69-4.364 1.126-1.165 2.577-1.748 4.346-1.748 1.775 0 3.22.583 4.347 1.748 1.126 1.165 1.69 2.621 1.69 4.364 0 1.748-.564 3.2-1.69 4.365Zm-4.35-.596c.915 0 1.633-.343 2.15-1.024.516-.686.779-1.597.779-2.739s-.259-2.058-.78-2.753c-.516-.69-1.234-1.038-2.15-1.038-.929 0-1.652.343-2.163 1.024-.512.686-.765 1.607-.765 2.762 0 1.142.253 2.058.765 2.74.511.685 1.234 1.028 2.164 1.028Zm7.505 2.006V21.928h3.065V38.05h-3.065Zm5.088-13.37v-2.753h3.065v2.753h-3.065Zm0 13.37V26.485h3.065V38.05h-3.065Zm10.411.339c-1.788 0-3.22-.578-4.304-1.739-1.08-1.155-1.625-2.617-1.625-4.374 0-1.757.53-3.218 1.587-4.374 1.056-1.155 2.45-1.738 4.178-1.738 1.455 0 2.642.385 3.557 1.151.916.766 1.479 1.795 1.69 3.091h-2.995a2.252 2.252 0 0 0-.722-1.287c-.376-.329-.84-.498-1.4-.498-.9 0-1.59.324-2.074.968-.479.648-.723 1.541-.723 2.683 0 1.127.235 2.02.7 2.673.465.653 1.15.982 2.051.982 1.338 0 2.112-.653 2.319-1.964h2.952c-.103 1.278-.624 2.335-1.553 3.166-.92.842-2.136 1.26-3.638 1.26Zm6.669 3.453v-2.415h1.08c1.14 0 1.713-.526 1.713-1.578 0-.512-.29-1.555-.877-3.134l-3.108-8.231h3.22l1.713 5.21.742 2.528h.047c.211-.977.437-1.818.676-2.528l1.624-5.21h3.088L93.9 38.347c-.451 1.325-.958 2.236-1.521 2.739-.564.503-1.418.756-2.558.756h-1.808ZM39.1 59.662V43.538h7.388c1.549 0 2.797.413 3.75 1.24.953.827 1.432 1.907 1.432 3.246 0 2.058-.986 3.36-2.953 3.9v.066c.765.225 1.343.582 1.723 1.07.385.49.629 1.213.732 2.176.028.362.066.785.103 1.273.038.489.066.874.09 1.16.023.287.051.574.089.856.037.286.089.507.16.667.065.16.154.258.258.305v.16H48.74a.374.374 0 0 1-.16-.17 1.16 1.16 0 0 1-.113-.347 8.433 8.433 0 0 1-.146-1.071c-.018-.249-.041-.465-.055-.653l-.057-.742-.056-.733c-.136-1.833-1.188-2.753-3.154-2.753h-2.638v6.474H39.1Zm3.267-13.484v4.487h3.468c.855 0 1.512-.202 1.972-.611.46-.404.685-.94.685-1.602 0-.677-.216-1.226-.652-1.645-.437-.422-1.075-.629-1.916-.629h-3.557Zm18.427 13.484c-.15-.198-.272-.625-.361-1.288h-.047a3.41 3.41 0 0 1-1.263 1.151c-.512.273-1.225.404-2.14.404-1.216 0-2.192-.31-2.93-.925-.736-.615-1.102-1.49-1.102-2.617 0-1.175.403-2.034 1.215-2.584.812-.55 1.953-.93 3.427-1.137 1.08-.15 1.816-.305 2.206-.46.39-.16.587-.442.587-.846 0-.423-.165-.756-.498-1.005-.333-.25-.812-.371-1.44-.371-1.4 0-2.141.54-2.23 1.625H53.49c.047-1.1.489-2.006 1.329-2.73.84-.723 2.056-1.08 3.652-1.08 3.243 0 4.867 1.419 4.867 4.261v5.887c0 .874.136 1.405.404 1.602v.113h-2.948Zm-3.06-1.87c.84 0 1.506-.216 1.994-.653.489-.437.733-.954.733-1.555v-1.739c-.329.198-1.042.423-2.14.677-.874.197-1.488.418-1.85.667-.361.25-.54.63-.54 1.137 0 .977.596 1.466 1.803 1.466ZM69.604 60c-1.455 0-2.638-.554-3.539-1.658-.901-1.105-1.352-2.59-1.352-4.454 0-1.804.46-3.275 1.385-4.407.925-1.137 2.108-1.701 3.549-1.701 1.44 0 2.53.573 3.266 1.715h.066v-5.957h3.065v16.124h-2.952v-1.513h-.047c-.746 1.236-1.892 1.85-3.44 1.85Zm.676-2.57c.901 0 1.587-.31 2.06-.925.475-.616.71-1.466.71-2.547 0-2.466-.892-3.697-2.68-3.697-.827 0-1.456.328-1.892.991-.437.662-.653 1.541-.653 2.64 0 1.128.216 2.002.643 2.617.428.611 1.033.921 1.812.921Zm15.03 2.232c-.15-.198-.272-.625-.361-1.288h-.047a3.41 3.41 0 0 1-1.263 1.151c-.511.273-1.225.404-2.14.404-1.216 0-2.192-.31-2.93-.925-.736-.615-1.102-1.49-1.102-2.617 0-1.175.404-2.034 1.216-2.584.811-.55 1.952-.93 3.426-1.137 1.08-.15 1.817-.305 2.206-.46.39-.16.587-.442.587-.846 0-.423-.165-.756-.498-1.005-.333-.25-.812-.371-1.44-.371-1.4 0-2.141.54-2.23 1.625h-2.727c.046-1.1.488-2.006 1.328-2.73.84-.723 2.056-1.08 3.652-1.08 3.243 0 4.867 1.419 4.867 4.261v5.887c0 .874.136 1.405.404 1.602v.113H85.31Zm-3.065-1.87c.84 0 1.507-.216 1.995-.653.488-.437.732-.954.732-1.555v-1.739c-.328.198-1.042.423-2.14.677-.873.197-1.488.418-1.85.667-.361.25-.54.63-.54 1.137 0 .977.602 1.466 1.803 1.466Zm10.5-9.697v1.851h.066c.361-.676.76-1.174 1.192-1.498.437-.325.986-.484 1.643-.484.314 0 .554.028.723.089v2.683h-.066c-1.037-.104-1.868.122-2.502.676-.629.555-.948 1.428-.948 2.617v5.638h-3.065V48.1h2.957v-.005Z"
      ></path>
      <mask
        id="a"
        style={{ maskType: 'alpha' }}
        maskUnits="userSpaceOnUse"
        x="0"
        y="0"
        width="30"
        height="60"
      >
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M0 30c0 16.54 13.45 30 29.97 30v-3.37A26.66 26.66 0 013.36 30 26.66 26.66 0 0129.97 3.36V0A30.02 30.02 0 000 30zm29.97 22.73A22.75 22.75 0 017.26 30 22.75 22.75 0 0129.97 7.26v3.36a19.38 19.38 0 000 38.75v3.36zM14.27 30c0 8.67 7.04 15.72 15.7 15.72v-3.36a12.36 12.36 0 010-24.71v-3.36c-8.66 0-15.7 7.05-15.7 15.71zm7.5 0a8.2 8.2 0 008.2 8.2v-3.36a4.84 4.84 0 010-9.68V21.8a8.2 8.2 0 00-8.2 8.2z"
          fill="#fff"
        ></path>
      </mask>
      <g mask="url(#a)">
        <path
          fill-rule="evenodd"
          clip-rule="evenodd"
          d="M0 30c0 16.54 13.45 30 29.97 30v-3.37A26.66 26.66 0 013.36 30 26.66 26.66 0 0129.97 3.36V0A30.02 30.02 0 000 30zm29.97 22.73A22.75 22.75 0 017.26 30 22.75 22.75 0 0129.97 7.26v3.36a19.38 19.38 0 000 38.75v3.36zM14.27 30c0 8.67 7.04 15.72 15.7 15.72v-3.36a12.36 12.36 0 010-24.71v-3.36c-8.66 0-15.7 7.05-15.7 15.71zm7.5 0a8.2 8.2 0 008.2 8.2v-3.36a4.84 4.84 0 010-9.68V21.8a8.2 8.2 0 00-8.2 8.2z"
          fill="#0ABAFA"
        ></path>
        <path
          d="M-49.6 48.42L-12.13 5.2l67.7 58.7L18.1 107.1l-67.7-58.7z"
          fill="#2371E1"
        ></path>
      </g>
    </svg>
  );
};
export default Logo;
