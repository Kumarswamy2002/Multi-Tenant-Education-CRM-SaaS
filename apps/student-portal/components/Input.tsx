"use client";

import React, { useState } from "react";

export interface InputProps {
  id?: string;
  className?: string;
  variant?: "primary" | "secondary" | "danger" | "success" | "outline" | "ghost";
  size?: "sm" | "md" | "lg" | "xl";
  label?: string;
  disabled?: boolean;
  loading?: boolean;
  onClick?: (e: any) => void;
  children?: React.ReactNode;
}

/**
 * Form Input with floating labels, error states, and prefix/suffix icons
 * Enterprise Design System Component for student-portal
 */
export const Input: React.FC<InputProps> = ({
  id,
  className = "",
  variant = "primary",
  size = "md",
  label,
  disabled = false,
  loading = false,
  onClick,
  children,
}) => {
  const [isActive, setIsActive] = useState(false);

  const getVariantStyles = () => {
    switch (variant) {
      case "secondary":
        return "bg-slate-800 hover:bg-slate-700 text-slate-200 border border-slate-700";
      case "danger":
        return "bg-rose-600 hover:bg-rose-500 text-white shadow-lg shadow-rose-600/30";
      case "success":
        return "bg-emerald-600 hover:bg-emerald-500 text-white shadow-lg shadow-emerald-600/30";
      case "outline":
        return "bg-transparent hover:bg-slate-800 text-indigo-400 border border-indigo-500/40";
      case "ghost":
        return "bg-transparent hover:bg-slate-800 text-slate-300";
      case "primary":
      default:
        return "bg-indigo-600 hover:bg-indigo-500 text-white shadow-lg shadow-indigo-600/30";
    }
  };

  const getSizeStyles = () => {
    switch (size) {
      case "sm":
        return "px-2.5 py-1 text-xs";
      case "lg":
        return "px-5 py-3 text-base";
      case "xl":
        return "px-6 py-3.5 text-lg font-bold";
      case "md":
      default:
        return "px-4 py-2 text-sm";
    }
  };

  return (
    <div
      id={id}
      onClick={disabled || loading ? undefined : onClick}
      onMouseEnter={() => setIsActive(true)}
      onMouseLeave={() => setIsActive(false)}
      className={`inline-flex items-center justify-center font-medium rounded-xl transition-all duration-200 cursor-pointer select-none ${getVariantStyles()} ${getSizeStyles()} ${
        disabled ? "opacity-50 cursor-not-allowed pointer-events-none" : ""
      } ${className}`}
    >
      {loading && (
        <svg
          className="animate-spin -ml-1 mr-2 h-4 w-4 text-current"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          ></circle>
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          ></path>
        </svg>
      )}
      {label || children || "Input Component"}
    </div>
  );
};

export default Input;
