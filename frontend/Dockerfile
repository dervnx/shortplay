FROM node:20-alpine AS base

# Use Chinese npm mirror
RUN npm config set registry https://registry.npmmirror.com

# Install dependencies only when needed
FROM base AS deps
WORKDIR /app
COPY package*.json ./
RUN npm install

# Development image
FROM base AS development
WORKDIR /app
COPY --from=deps /app/node_modules ./node_modules
COPY . .
EXPOSE 3000
CMD ["npm", "run", "dev"]

# Build image
FROM deps AS build
WORKDIR /app
COPY . .
RUN npm run build

# Production image
FROM base AS production
WORKDIR /app
ENV NODE_ENV=production
COPY --from=deps /app/node_modules ./node_modules
COPY --from=build /app/package*.json ./
COPY --from=build /app/dist ./dist
COPY --from=build /app/vite.config.ts ./
EXPOSE 3000
CMD ["node", "/app/node_modules/vite/bin/vite.js", "preview", "--host", "0.0.0.0", "--port", "3000"]
