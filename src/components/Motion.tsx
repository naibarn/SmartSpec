import { motion, type HTMLMotionProps } from 'framer-motion';
import type { ReactNode } from 'react';

// Fade In Animation
interface FadeInProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
  delay?: number;
  duration?: number;
}

export function FadeIn({ children, delay = 0, duration = 0.5, ...props }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration, delay }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Slide In From Left
export function SlideInLeft({ children, delay = 0, duration = 0.5, ...props }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: -50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration, delay, type: 'spring', stiffness: 100 }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Slide In From Right
export function SlideInRight({ children, delay = 0, duration = 0.5, ...props }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, x: 50 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration, delay, type: 'spring', stiffness: 100 }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Scale In Animation
export function ScaleIn({ children, delay = 0, duration = 0.3, ...props }: FadeInProps) {
  return (
    <motion.div
      initial={{ opacity: 0, scale: 0.8 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration, delay, type: 'spring', stiffness: 200 }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Stagger Children Animation
interface StaggerContainerProps extends HTMLMotionProps<"div"> {
  children: ReactNode;
  staggerDelay?: number;
}

export function StaggerContainer({ children, staggerDelay = 0.1, ...props }: StaggerContainerProps) {
  return (
    <motion.div
      initial="hidden"
      animate="visible"
      variants={{
        hidden: { opacity: 0 },
        visible: {
          opacity: 1,
          transition: {
            staggerChildren: staggerDelay,
          },
        },
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Stagger Item (use inside StaggerContainer)
export function StaggerItem({ children, ...props }: HTMLMotionProps<"div">) {
  return (
    <motion.div
      variants={{
        hidden: { opacity: 0, y: 20 },
        visible: { opacity: 1, y: 0 },
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Hover Scale Animation
export function HoverScale({ children, scale = 1.05, ...props }: FadeInProps & { scale?: number }) {
  return (
    <motion.div
      whileHover={{ scale }}
      whileTap={{ scale: 0.95 }}
      transition={{ type: 'spring', stiffness: 400, damping: 17 }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Bounce Animation
export function Bounce({ children, ...props }: HTMLMotionProps<"div">) {
  return (
    <motion.div
      animate={{
        y: [0, -10, 0],
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Pulse Animation
export function Pulse({ children, ...props }: HTMLMotionProps<"div">) {
  return (
    <motion.div
      animate={{
        scale: [1, 1.05, 1],
      }}
      transition={{
        duration: 2,
        repeat: Infinity,
        ease: 'easeInOut',
      }}
      {...props}
    >
      {children}
    </motion.div>
  );
}

// Page Transition
export function PageTransition({ children, ...props }: HTMLMotionProps<"div">) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3 }}
      {...props}
    >
      {children}
    </motion.div>
  );
}
