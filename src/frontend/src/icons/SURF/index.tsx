import type React from "react";
import { forwardRef } from "react";
import SvgSURF from "./surf";

export const SURFIcon = forwardRef<
  SVGSVGElement,
  React.PropsWithChildren<{}>
>((props, ref) => {
  return <SvgSURF ref={ref} {...props} />;
});
